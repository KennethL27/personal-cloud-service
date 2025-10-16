from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable is not set")

    ALGORITHM = os.getenv("JWT_ALGORITHM")
    if not ALGORITHM:
        raise ValueError("JWT_ALGORITHM environment variable is not set")

    access_token_expire_minutes_str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    if not access_token_expire_minutes_str:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES environment variable is not set")
    try:
        ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_expire_minutes_str)
    except (TypeError, ValueError):
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES environment variable must be an integer")
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token."""
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable is not set")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    if not ALGORITHM:
        raise ValueError("JWT_ALGORITHM environment variable is not set")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_password_hash(password: str) -> str:
    """Hash a password (not used for Google OAuth, but included for completeness)."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password (not used for Google OAuth, but included for completeness)."""
    return pwd_context.verify(plain_password, hashed_password)
