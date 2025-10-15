from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from src.api.auth.dependencies import get_current_user

router = APIRouter(tags=["Authentication"])

class VerifyResponse(BaseModel):
    authenticated: bool
    user: Optional[dict] = None

@router.get('/', response_model=VerifyResponse)
async def verify_auth(current_user: dict = Depends(get_current_user)):
    """Verify current authentication status."""
    return VerifyResponse(
        authenticated=True,
        user=current_user
    )
