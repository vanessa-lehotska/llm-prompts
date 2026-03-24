"""Handler for Prompt Injection Challenge mode"""
from fastapi import HTTPException
from typing import Dict, Any

from models import ChatRequest, ChatResponse
from config import get_mode_config, get_level_config
from utils.defenses import filter_response, check_secret_match, detect_prompt_injection_attempt
from utils.openai_client import call_openai_api


async def handle_prompt_injection(request: ChatRequest, config: Dict[str, Any]) -> ChatResponse:
    """
    Handle prompt injection mode with different defense layers.
    
    Each level implements progressively stronger defenses:
    - Level 1: Minimal system prompt (no defense)
    - Level 2: Basic system prompt (clearer instructions)
    - Level 3: System prompt hardening (explicit warnings)
    - Level 4: Input guard (heuristic prompt-injection detection)
    - Level 5: Response filtering (blocks secret in output)
    - Level 6: Combined defense (input guard + response filtering)
    """
    mode_config = get_mode_config(config, "prompt_injection")
    if not mode_config:
        raise HTTPException(status_code=500, detail="Prompt injection mode not configured")
    
    try:
        level_config = get_level_config(mode_config, request.difficulty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    system_prompt = level_config.get("systemPrompt", "")
    secret = level_config.get("secret", "")
    defense = level_config.get("defense", "none")
    
    # Apply input guard for obvious prompt-injection attempts
    user_message = request.user_message
    if defense in ["input_guard", "combined"] and detect_prompt_injection_attempt(user_message):
        return ChatResponse(
            response="I cannot process instruction-manipulation requests.",
            level_up=False,
            current_level=request.difficulty,
            defense=defense
        )
    
    # Check if user found the secret
    if secret and check_secret_match(user_message, secret):
        return _handle_level_completion(secret, request.difficulty, mode_config)
    
    # Generate AI response
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    response = call_openai_api(messages)
    
    try:
        content = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid response from OpenAI: {str(e)}")
    
    # Apply response filtering if defense requires it
    if defense in ["response_filtering", "combined"]:
        content = filter_response(content, secret)
    
    return ChatResponse(
        response=content,
        level_up=False,
        current_level=request.difficulty,
        defense=defense
    )


def _handle_level_completion(secret: str, current_level: int, mode_config: Dict[str, Any]) -> ChatResponse:
    """Handle level completion and determine if game is finished"""
    levels = mode_config.get("levels", {})
    max_level = max([int(k) for k in levels.keys()]) if levels else 0
    next_level = current_level + 1
    
    if next_level <= max_level:
        return ChatResponse(
            response=f"Correct! The secret was '{secret}'. Continue to Level {next_level}.",
            level_up=True,
            current_level=current_level,
            next_level=next_level
        )
    else:
        return ChatResponse(
            response=f"Congratulations! You found the final secret '{secret}'! You have completed all levels!",
            level_up=False,
            current_level=current_level,
            game_completed=True
        )
