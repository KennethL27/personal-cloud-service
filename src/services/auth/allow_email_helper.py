import os
import json

def is_email_allowed(email: str) -> bool:
    """Check if an email is in the allowed list."""
    if not email:
        return False

    ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS")
    if not ALLOWED_EMAILS:
        raise ValueError("ALLOWED_EMAILS environment variable not set")
    
    allowed_emails = json.loads(ALLOWED_EMAILS)
    return email.lower() in [allowed.lower() for allowed in allowed_emails]
