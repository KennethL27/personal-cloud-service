from fastapi import HTTPException, status, Cookie
from typing import Optional, Dict, Any
from src.services.auth.jwt_helper import verify_token
from src.services.auth.allow_email_helper import is_email_allowed

def create_unauthorized_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

def create_forbidden_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )

async def get_current_user(token: Optional[str] = Cookie(None, alias="access_token")) -> Dict[str, Any]:
    """FastAPI dependency to get current authenticated user from JWT cookie."""
    if not token:
        raise create_unauthorized_exception("Not authenticated")
    
    # Verify the token
    payload = verify_token(token)
    if payload is None:
        raise create_unauthorized_exception("Invalid authentication credentials")
    
    # Extract user info from token
    email: str = payload.get("sub")  # 'sub' contains the email
    if email is None:
        raise create_unauthorized_exception("Invalid token payload")
    
    # Double-check that the email is still allowed (in case config changed)
    if not is_email_allowed(email):
        raise create_forbidden_exception("Your email is not authorized to access this service")
    
    return {
        "email": email,
        "name": payload.get("name"),
        "picture": payload.get("picture"),
        "sub": payload.get("sub")
    }
