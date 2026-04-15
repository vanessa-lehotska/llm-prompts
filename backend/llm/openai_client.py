import os

from openai import OpenAI


def get_model_name() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found.")
    return OpenAI(api_key=api_key)


def call_openai_api(
    messages: list[dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 500,
) -> str:
    client = get_openai_client()
    model_name = get_model_name()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    except Exception as exc:
        raise RuntimeError(f"OpenAI API call failed: {exc}") from exc