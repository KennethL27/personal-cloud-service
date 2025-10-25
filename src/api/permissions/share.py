from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from src.api.auth.dependencies import get_current_user
from src.services.database.user_settings import get_user_setting, update_user_setting, create_user_setting
from src.services.database.users import get_user_by_email, create_user, update_user

router = APIRouter(tags=["Permissions"])

class ShareForm(BaseModel):
    name: str = Field(..., description="Name of User", example="First Last")
    email: str = Field(..., description="Email for User", example="firstlast@example.com")
    hard_drive_path_selection: str = Field(..., description="Drive path", example="Volume/device_1")

@router.put('/')
async def share(
        payload: ShareForm,
        current_user: dict = Depends(get_current_user)
    ):
    """Create or Update User for sharing a specific file path on the drive"""
    email = current_user.get("email")
    user = get_user_by_email(email)

    if not user.is_admin:
         raise HTTPException(status_code=401, detail="Unauthorized sharing access")

    form_email = payload.email
    form_user = get_user_by_email(form_email)

    if not form_user:
        user_payload = {
            "email": form_email,
            "name": payload.name,
            "is_admin": False,
            "is_guest": True
        }
        new_form_user = create_user(user_payload)

        user_setting_payload = {
            "user_id": new_form_user.id,
            "hard_drive_path_selection": payload.hard_drive_path_selection
        }
        create_user_setting(user_setting_payload)

        return {"status": "ok"}

    update_user({
        "email": form_user.email,
        "name": payload.name,
        "is_admin": False,
        "is_guest": True
    })

    user_setting = get_user_setting(form_user.id)
    if not user_setting:
        create_user_setting({
                            "user_id": form_user.id,
                            "hard_drive_path_selection": payload.hard_drive_path_selection
                            })
        return {"status": "ok"}
    
    update_user_setting({
        "user_id": form_user.id,
        "hard_drive_path_selection": payload.hard_drive_path_selection
    })

    return {"status": "ok"}