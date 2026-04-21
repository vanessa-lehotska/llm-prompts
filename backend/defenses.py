"""Defense mechanisms for LLM security (simple heuristic-based approach)"""

import re


# --- INJECTION PATTERNS ---
_INJECTION_PATTERNS = [
    # instruction override
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|prior)\s+instructions?",

    # system probing
    r"system\s+prompt",
    r"developer\s+mode",
    r"jailbreak",

    # direct secret extraction
    r"reveal\s+(the\s+)?(secret|password)",
    r"tell\s+me\s+(the\s+)?(secret|password)",
    r"what\s+is\s+(the\s+)?(secret|password)",

    # bypass attempts
    r"bypass\s+(safety|rules|guardrails?)",

    # transformations
    r"encode|decode|base64|rot13",
    r"reverse|backwards",
    r"spell\s+it",

    # indirect hints
    r"first\s+letter",
    r"give\s+me\s+a\s+hint",
    r"describe\s+the\s+secret",

    # roleplay attacks
    r"pretend\s+you\s+are",
    r"imagine\s+you\s+are",
]

_INJECTION_REGEXES = [re.compile(pattern) for pattern in _INJECTION_PATTERNS]


def detect_prompt_injection_attempt(prompt: str) -> bool:
    """Detect prompt injection attempts using heuristics."""
    # strip invisible zero-width chars to prevent regex bypass
    normalized = re.sub(r'[\u200B-\u200D\uFEFF]', '', prompt).lower()

    for regex in _INJECTION_REGEXES:
        if regex.search(normalized):
            return True
    return False


def output_guard(response: str, secret: str) -> str:
    """Block response if it likely contains the secret."""
    resp = response.lower()
    sec = secret.lower()

    if sec in resp:                  # exact match
        return "I cannot reveal that information."
    if " ".join(sec) in resp:        # spaced (E L E P H A N T)
        return "I cannot reveal that information."
    if sec[::-1] in resp:            # reversed (TNAHPELE)
        return "I cannot reveal that information."
    return response


def check_secret_match(user_message: str, secret: str) -> bool:
    """Check if user guessed the secret."""
    return secret.lower() in user_message.lower()