from fastapi import APIRouter
from pathlib import Path
from fastapi import Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from src.services.api.file.file_helper import bytes_to_human_readable, is_hidden
from src.api.auth.dependencies import get_current_user
from src.services.database.users import get_user_by_email
from src.services.database.user_settings import get_user_setting

router = APIRouter(tags=["File"])

@router.get("/")
def list_folder_items(
    path: str = Query(default="", description="Optional relative path"),
    current_user: dict = Depends(get_current_user),
    ):
    """
    List non-hidden files and folders in the specified directory (non-recursive).
    The path is appended safely to the User's drive selection.
    """

    email = current_user.get("email")
    user = get_user_by_email(email)
    user_setting = get_user_setting(user.id)

    default_path = user_setting.hard_drive_path_selection
    base = Path(default_path).resolve()
    target_path = (base / path).resolve()

    # Prevent directory traversal outside BASE_PATH
    if not str(target_path).startswith(str(base)):
        raise HTTPException(status_code=404, detail="Directory not found: outside of base directory")

    # Check that the path exists and is a directory
    if not target_path.exists():
        raise HTTPException(status_code=404, detail=f"Directory not found: {target_path}")
    if not target_path.is_dir():
        raise HTTPException(status_code=400, detail=f"Path is not a directory: {target_path}")

    entries = []
    try:
        for item in target_path.iterdir():
            if is_hidden(item):
                continue

            entry = {
                "name": item.name,
                "full_path": str(item.resolve()),
                "relative_path": str(item.relative_to(base)),
                "type": "folder" if item.is_dir() else "file",
                "size": None,
                "modified": datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            }

            if item.is_file():
                entry["size"] = bytes_to_human_readable(item.stat().st_size)

            entries.append(entry)

        return entries

    except PermissionError:
        raise HTTPException(status_code=403, detail=f"Permission denied: {target_path}")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "path": str(target_path)})
