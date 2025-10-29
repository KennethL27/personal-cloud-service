from fastapi import APIRouter, Depends
from src.api.auth.dependencies import get_current_user
from src.services.database.users import get_user_by_email

router = APIRouter(tags=["Permissions"])

@router.get('/')
async def admin_check(current_user: dict = Depends(get_current_user)):
    email = current_user.get("email")
    user = get_user_by_email(email)

    if not user:
        return {"is_admin": False}

    if not user.is_admin:
        return {"is_admin": False}

    return {"is_admin": True}
