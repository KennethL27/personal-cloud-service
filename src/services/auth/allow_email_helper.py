import os
import json

_cached_allowed_emails_set = None

def is_email_allowed(email: str) -> bool:
    global _cached_allowed_emails_set
    if not email:
        return False
    if _cached_allowed_emails_set is None:
        ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS")
        if not ALLOWED_EMAILS:
            raise ValueError("ALLOWED_EMAILS environment variable not set")
        try:
            allowed_emails = json.loads(ALLOWED_EMAILS)
        except json.JSONDecodeError as e:
            raise ValueError("ALLOWED_EMAILS environment variable is not valid JSON") from e
        if not isinstance(allowed_emails, list):
            raise ValueError("ALLOWED_EMAILS environment variable must be a JSON list")
        _cached_allowed_emails_set = set(allowed.lower() for allowed in allowed_emails if isinstance(allowed, str))
    return email.lower() in _cached_allowed_emails_set
