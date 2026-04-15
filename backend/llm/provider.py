import logging
import time

from fastapi import HTTPException

from llm.anthropic_client import call_anthropic_api, extract_anthropic_text
from llm.openai_client import call_openai_api, extract_openai_text

logger = logging.getLogger(__name__)


def call_llm(messages: list[dict[str, str]], provider: str) -> str:
    provider_name = provider.lower()
    max_retries = 3
    delay_seconds = 2

    for attempt in range(max_retries):
        try:
            if provider_name == "anthropic":
                response = call_anthropic_api(messages)
                return extract_anthropic_text(response)

            if provider_name == "openai":
                response = call_openai_api(messages)
                return extract_openai_text(response)

            raise RuntimeError(f"Unsupported LLM provider: {provider}")

        except Exception as exc:
            logger.exception(
                "LLM call failed for provider '%s' on attempt %s/%s",
                provider_name,
                attempt + 1,
                max_retries,
            )

            is_last_attempt = attempt == max_retries - 1
            if is_last_attempt:
                raise HTTPException(
                    status_code=500,
                    detail=f"LLM provider error: {str(exc)}",
                ) from exc

            time.sleep(delay_seconds)
            delay_seconds *= 2