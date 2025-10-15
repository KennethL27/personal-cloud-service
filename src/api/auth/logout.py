from fastapi import APIRouter, Response
from pydantic import BaseModel

router = APIRouter(tags=["Authentication"])

class LogoutResponse(BaseModel):
    message: str

@router.post('/', response_model=LogoutResponse)
async def logout(response: Response):
    """Logout and clear authentication cookie."""
    response.delete_cookie(key="access_token")
    return LogoutResponse(message="Logout successful")
