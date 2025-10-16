from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel
from src.services.auth.google_helper import verify_google_token
from src.services.auth.jwt_helper import create_access_token
from src.services.auth.allow_email_helper import is_email_allowed
import os

router = APIRouter(tags=["Authentication"])

class LoginRequest(BaseModel):
    token: str

class LoginResponse(BaseModel):
    message: str
    user: dict

@router.post('/', response_model=LoginResponse)
async def login(request: LoginRequest, response: Response):
    """Login with Google OAuth token."""
    user_info = verify_google_token(request.token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )
    
    email = user_info.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not found in Google token"
        )
    
    # Check if email is allowed
    if not is_email_allowed(email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your email is not authorized to access this service"
        )
    
    # Create JWT token
    token_data = {
        "sub": email,
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
        "email_verified": user_info.get("email_verified", False)
    }
    
    access_token = create_access_token(data=token_data)
    
    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not (os.getenv("ENV", "development").lower() in ["development", "dev", "local", "test"]),
        samesite="lax",
        max_age=3600  # 1 hour
    )
    
    return LoginResponse(
        message="Login successful",
        user={
            "email": email,
            "name": user_info.get("name"),
            "picture": user_info.get("picture")
        }
    )
