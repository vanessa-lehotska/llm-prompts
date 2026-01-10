"""OpenAI API client wrapper"""
import os
from fastapi import HTTPException
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY not found in .env file!")

client = OpenAI(api_key=openai_api_key)


def call_openai_api(messages: list, temperature: float = 0.7, max_tokens: int = 500):
    """
    Call OpenAI API using the official SDK.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens in response
    
    Returns:
        OpenAI API response object
    
    Raises:
        HTTPException: If API call fails
    """
    try:
        response = client.chat.completions.create(
            model=openai_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "OpenAI API error",
                "message": str(e)
            }
        )


def get_model_name() -> str:
    """Get the configured OpenAI model name"""
    return openai_model
