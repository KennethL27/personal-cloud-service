from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
from src.services.api.file_upload import get_external_drive_path
import mimetypes

router = APIRouter(tags=["Steam File"])

@router.get('/')
async def stream(file_name: str):
    file_path = Path(f"{get_external_drive_path()}{folder_destination(file_name.split('.')[-1])}/{file_name}")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    mime_type, _ = mimetypes.guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"

    return StreamingResponse(iterfile(file_path), media_type=mime_type)

def iterfile(file_path):
    with open(file_path, mode="rb") as file_like:
        while chunk := file_like.read(1024 * 1024):
            yield chunk
            
def folder_destination(file_type):
    if file_type in ['jpeg', 'jpg']:
        return "/photos"
    elif file_type in ['mp4', 'mov']:
        return "/videos"
    elif file_type == 'mpeg':
        return "/audio"
    elif file_type == 'pdf':
        return "/documents"
    elif file_type == 'zip':
        return "/zip"
    else:
        return "/others"
    
