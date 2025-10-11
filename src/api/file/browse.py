from fastapi import APIRouter, Query
from src.services.api.file_path_helper import get_external_drive_path, get_folder_destination
from typing import List, Optional
import os
import mimetypes
from datetime import datetime

router = APIRouter(tags=["File Browse"])

@router.get('/')
async def browse(category: Optional[str] = Query(None, description="Filter by folder type (photos, videos, documents, audio, zip, others)")):
    base_path = get_external_drive_path()
    if not base_path:
        return {"files": [], "total_count": 0}
    
    # Define all possible categories
    categories = ["photos", "videos", "documents", "audio", "zip", "others"]
    
    # If category is specified, validate it
    if category and category not in categories:
        return {"files": [], "total_count": 0}
    
    # Determine which categories to scan
    categories_to_scan = [category] if category else categories
    
    files = []
    
    for cat in categories_to_scan:
        folder_path = os.path.join(base_path, cat)
        
        # Check if folder exists
        if not os.path.exists(folder_path):
            continue
            
        try:
            # List files in the category folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                # Skip directories
                if os.path.isdir(file_path):
                    continue
                
                try:
                    # Get file metadata
                    stat = os.stat(file_path)
                    file_size = stat.st_size
                    modified_time = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    
                    # Guess MIME type
                    mime_type, _ = mimetypes.guess_type(file_path)
                    mime_type = mime_type or "application/octet-stream"
                    
                    files.append({
                        "name": filename,
                        "size": file_size,
                        "type": mime_type,
                        "modified": modified_time,
                        "category": cat
                    })
                    
                except (OSError, IOError):
                    # Skip files that can't be accessed
                    continue
                    
        except (OSError, IOError):
            # Skip folders that can't be accessed
            continue
    
    return {
        "files": files,
        "total_count": len(files)
    }
