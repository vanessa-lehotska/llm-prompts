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
):
    from openai import error as openai_error
    client = get_openai_client()
    model_name = get_model_name()

    try:
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except openai_error.RateLimitError:
        return {"error": "API key limit reached. Please try again later."}
    except openai_error.InvalidRequestError as e:
        if "maximum context length" in str(e):
            return {"error": "Token limit exceeded. Please shorten your input."}
        else:
            raise


def extract_openai_text(response) -> str:
    content = response.choices[0].message.content
    return content or ""