import os
from typing import Optional, Dict, Any
from google.oauth2 import id_token
from google.auth.transport import requests

def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a Google OAuth token and return user info."""
    try:
        # Get Google Client ID from environment
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        if not client_id:
            raise ValueError("GOOGLE_CLIENT_ID environment variable not set")
        
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            client_id
        )
        
        # Extract user information
        user_info = {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "picture": idinfo.get("picture"),
            "sub": idinfo.get("sub"),  # Google user ID
            "email_verified": idinfo.get("email_verified", False)
        }
        
        # Verify email is verified by Google
        if not user_info["email_verified"]:
            return None
            
        return user_info
        
    except ValueError as e:
        # Invalid token
        return None
    except Exception as e:
        # Other errors
        return None
