from fastapi import APIRouter, File, UploadFile
from src.services.api.file_path_helper import get_external_drive_path, get_folder_destination
from typing import List
import shutil
import os

router = APIRouter(tags=["File Upload"])

@router.post('/')
async def upload(files: List[UploadFile] = File(...)):
    uploaded_filenames = []

    for file in files:
        UPLOAD_DIR = get_external_drive_path() + get_folder_destination(file.content_type)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            try:
                shutil.copyfileobj(file.file, buffer)
            except Exception as e:
                return {"status": "error", "message": f"Unexpected error occurred: {e}"}
        
        uploaded_filenames.append(file.filename)
    
    return {"uploaded_files": uploaded_filenames}
