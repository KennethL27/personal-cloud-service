from fastapi import APIRouter, File, UploadFile, Form
from typing import List
import shutil
from pathlib import Path

router = APIRouter(tags=["File"])

@router.post('/')
async def upload(
    file_path_location: str = Form(...),
    files: List[UploadFile] = File(...)
    ):
    """Upload your file to the drive given a path"""
    uploaded_filenames = []

    for file in files:
        file_location = Path(file_path_location) / file.filename
        with open(file_location, "wb") as buffer:
            try:
                shutil.copyfileobj(file.file, buffer)
            except Exception as e:
                return {"status": "error", "message": f"Unexpected error occurred: {e}"}
        
        uploaded_filenames.append(file.filename)
    
    return {"uploaded_files": uploaded_filenames}
