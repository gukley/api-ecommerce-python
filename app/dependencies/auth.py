from fastapi import Depends, HTTPException
from app.models.user_model import User, UserRole
from app.core.middlewares.auth_middleware import get_current_user


def is_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user


def is_moderator(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.MODERATOR.value, UserRole.ADMIN.value]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user
