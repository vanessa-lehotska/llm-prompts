import os

from anthropic import Anthropic


def get_anthropic_model_name() -> str:
    return os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


def get_anthropic_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not found.")

    return Anthropic(api_key=api_key)


def call_anthropic_api(
    messages: list[dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 500,
):
    system_prompt = None
    filtered_messages: list[dict[str, str]] = []

    for message in messages:
        content = (message.get("content") or "").strip()
        if not content:
            continue

        role = message.get("role")
        if role == "system":
            system_prompt = content
            continue

        if role in {"user", "assistant"}:
            filtered_messages.append(
                {
                    "role": role,
                    "content": content,
                }
            )

    kwargs = {
        "model": get_anthropic_model_name(),
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": filtered_messages,
    }

    if system_prompt:
        kwargs["system"] = system_prompt

    client = get_anthropic_client()
    return client.messages.create(**kwargs)


def extract_anthropic_text(response) -> str:
    parts = []

    for block in response.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)

    return "".join(parts).strip()