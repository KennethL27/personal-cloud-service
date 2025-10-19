from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import Optional
from src.services.database.users import get_user_by_email
from src.services.database.user_settings import get_user_setting, create_user_setting, update_user_setting
from src.api.auth.dependencies import get_current_user

router = APIRouter(tags=["File"])

class UserSettings(BaseModel):
    hard_drive_path_selection: str = Field(..., description="Drive path", example="Volume/device_1")

class UserSettingModel(BaseModel):
    id: int = Field(..., description="id value of the user settings", example=1)
    user_id: int = Field(..., description="user id value of the user", example=1)
    hard_drive_path_selection: str = Field(..., description="hard drive path for user", example="Volume/device_1")
    created_at: datetime = Field(..., description="created at timestamp", example="2025-01-01 10:10:10")
    updated_at: datetime = Field(..., description="updated at timestamp", example="2025-01-01 10:10:10")

@router.put('/')
async def user_settings(
        payload: UserSettings,
        current_user: dict = Depends(get_current_user)
    ):
    """Create or Update User Settings based off email from cookie (access token)"""
    
    email = current_user.get("email")
    user = get_user_by_email(email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_setting = get_user_setting(user.id)
    if not user_setting:
        create_user_setting({
                            "user_id": user.id,
                            "hard_drive_path_selection": payload.hard_drive_path_selection
                            })
        return {"status": "ok"}

    update_user_setting({
        "user_id": user.id,
        "hard_drive_path_selection": payload.hard_drive_path_selection
    }) 

    return {"status": "ok"}

@router.get('/', response_model=Optional[UserSettingModel])
async def user_settings(
        current_user: dict = Depends(get_current_user),
    ):
    """Get User Settings for the current user based off email from Cookie (access token)"""

    email = current_user.get("email")
    user = get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_setting = get_user_setting(user.id)

    if not user_setting:
        return None
    
    return UserSettingModel(
        id=user_setting.id,
        user_id=user_setting.user_id,
        hard_drive_path_selection=user_setting.hard_drive_path_selection,
        created_at=user_setting.created_at,
        updated_at=user_setting.updated_at
    )
