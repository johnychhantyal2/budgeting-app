#/app/core/admin.py

from fastapi import Depends, HTTPException, status
from ..core.security import get_current_active_user
from ..models.user import User

async def get_current_super_user(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user