from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
from src.api.auth.dependencies import get_current_user
from src.services.database.users import get_user_by_email
from src.services.database.user_settings import get_user_setting
import mimetypes

router = APIRouter(tags=["File"])

@router.get('/')
async def stream(
    file_name: str,
    current_user: dict = Depends(get_current_user)
    ):
    """Stream a file that exists on the drive"""
    email = current_user.get("email")
    user = get_user_by_email(email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_setting = get_user_setting(user.id)
    if not user_setting:
        raise HTTPException(status_code=404, detail="Default Path Section not found")

    default_path = user_setting.hard_drive_path_selection
    file_path = Path(Path(default_path) / Path(file_name)).resolve()
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    mime_type, _ = mimetypes.guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"

    return StreamingResponse(iterfile(file_path), media_type=mime_type)

def iterfile(file_path):
    with open(file_path, mode="rb") as file_like:
        while chunk := file_like.read(1024 * 1024):
            yield chunk
