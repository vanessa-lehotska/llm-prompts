"""Defense mechanisms for LLM security"""
import unicodedata
import re


# Common prompt-injection / jailbreak markers used for lightweight detection.
_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|prior)\s+instructions?",
    r"system\s+prompt",
    r"developer\s+mode",
    r"jailbreak",
    r"reveal\s+(the\s+)?(secret|password)",
    r"tell\s+me\s+(the\s+)?(secret|password)",
    r"what\s+is\s+(the\s+)?(secret|password)",
    r"bypass\s+(safety|rules|guardrails?)",
]


def detect_prompt_injection_attempt(prompt: str) -> bool:
    """
    Detect obvious prompt-injection patterns in user input.

    This is a heuristic defense for game progression, not a perfect classifier.
    """
    # Normalize and remove zero-width chars to reduce simple obfuscation.
    normalized = unicodedata.normalize('NFKC', prompt)
    normalized = re.sub(r'[\u200B-\u200D\uFEFF]', '', normalized).lower()

    for pattern in _INJECTION_PATTERNS:
        if re.search(pattern, normalized):
            return True

    return False


def filter_response(response: str, secret: str) -> str:
    """
    Response filtering - check if response contains secret and block it.
    
    This defense layer validates model output before sending to user.
    """
    if secret.upper() in response.upper():
        return "I cannot reveal that information."
    return response


def check_secret_match(user_message: str, secret: str) -> bool:
    """Check if user message contains the secret (case-insensitive)"""
    return secret.upper() in user_message.upper()
