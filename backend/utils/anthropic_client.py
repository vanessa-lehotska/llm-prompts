"""Anthropic API client wrapper"""
import os
import requests

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")

if not ANTHROPIC_API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY not found in .env file!")

API_URL = "https://api.anthropic.com/v1/messages"


def call_anthropic_api(messages: list, temperature: float = 0.7, max_tokens: int = 500):
    """
    Call Anthropic API using HTTP requests.
    messages: list of dicts with 'role' and 'content' (same as OpenAI format)
    """
    # Anthropic expects a single string prompt, so we concatenate user/assistant turns
    prompt = ""
    for m in messages:
        if m["role"] == "system":
            prompt += f"\n\nSystem: {m['content']}"
        elif m["role"] == "user":
            prompt += f"\n\nHuman: {m['content']}"
        elif m["role"] == "assistant":
            prompt += f"\n\nAssistant: {m['content']}"
    prompt = prompt.strip()

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
