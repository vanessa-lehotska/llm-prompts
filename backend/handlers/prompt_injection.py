import os
from typing import Any

from fastapi import HTTPException

from config import get_level_config, get_mode_config
from defenses import (
    check_secret_match,
    detect_prompt_injection_attempt,
    output_guard,
)
from llm.provider import call_llm
from models import ChatRequest, ChatResponse


def get_last_user_message(request: ChatRequest) -> str:
    if request.messages:
        for message in reversed(request.messages):
            if message.role == "user":
                return message.content
        return ""
    return request.user_message or ""


def _build_messages(system_prompt: str, request: ChatRequest) -> list[dict[str, str]]:
    if request.messages:
        chat_messages = [{"role": "system", "content": system_prompt}]
        chat_messages.extend(
            {"role": message.role, "content": message.content}
            for message in request.messages
        )
        return chat_messages

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": request.user_message or ""},
    ]


async def handle_prompt_injection(
    request: ChatRequest, config: dict[str, Any]
) -> ChatResponse:
    mode_config = get_mode_config(config, "prompt_injection")
    if not mode_config:
        raise HTTPException(status_code=500, detail="Configuration missing")

    try:
        level_config = get_level_config(mode_config, request.difficulty)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    system_prompt = level_config.get("systemPrompt", "")
    secret = level_config.get("secret", "")
    defense = level_config.get("defense", "none")

    latest_user_message = get_last_user_message(request)

    if defense in ["input_guard", "combined"]:
        if detect_prompt_injection_attempt(latest_user_message):
            return ChatResponse(
                response="I cannot process that request.",
                level_up=False,
                current_level=request.difficulty,
                defense=defense,
            )

    if secret and check_secret_match(latest_user_message, secret):
        return _handle_level_completion(secret, request.difficulty, mode_config)

    messages = _build_messages(system_prompt, request)
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    content = call_llm(messages, llm_provider)

    if defense in ["output_guard", "combined"]:
        content = output_guard(content, secret)

    return ChatResponse(
        response=content,
        level_up=False,
        current_level=request.difficulty,
        defense=defense,
    )


def _handle_level_completion(
    secret: str, current_level: int, mode_config: dict[str, Any]
) -> ChatResponse:
    levels = mode_config.get("levels", {})
    max_level = max(int(level) for level in levels) if levels else 0
    next_level = current_level + 1

    if next_level <= max_level:
        return ChatResponse(
            response=f"Correct! The secret was '{secret}'. Continue to Level {next_level}.",
            level_up=True,
            current_level=current_level,
            next_level=next_level,
        )

    return ChatResponse(
        response=f"Congratulations! You found the final secret '{secret}'!",
        level_up=False,
        current_level=current_level,
        game_completed=True,
    )