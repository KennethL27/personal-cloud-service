from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
from src.services.api.file_path_helper import get_external_drive_path, get_folder_destination
import mimetypes

router = APIRouter(tags=["File"])

@router.get('/')
async def stream(file_name: str):
    """Stream any file that exist on the drive"""
    file_path = Path(f"{get_external_drive_path()}{get_folder_destination(file_name.split('.')[-1])}/{file_name}")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    mime_type, _ = mimetypes.guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"

    return StreamingResponse(iterfile(file_path), media_type=mime_type)

def iterfile(file_path):
    with open(file_path, mode="rb") as file_like:
        while chunk := file_like.read(1024 * 1024):
            yield chunk
