"""Defense mechanisms for LLM security"""
import unicodedata
import re


def sanitize_input(prompt: str) -> str:
    """
    Input sanitization - remove zero-width characters and normalize Unicode.
    
    This defense layer cleans user input before it reaches the model.
    """
    # Normalize Unicode to canonical form
    prompt = unicodedata.normalize('NFKC', prompt)
    
    # Remove zero-width characters that could be used for hiding content
    prompt = re.sub(r'[\u200B-\u200D\uFEFF]', '', prompt)
    
    return prompt


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
