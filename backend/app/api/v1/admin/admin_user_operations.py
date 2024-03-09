# app/api/v1/admin/admin_auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from ....core.admin import get_current_super_user
from ....schemas.user import UserPublic, UserRoleUpdate
import logging
from ....core.security import get_current_active_user
from ....models.user import User
from typing import List
from ....crud.crud_admin import get_all_users, update_user_role
from ....crud.crud_user import get_user_by_username
from sqlalchemy.orm import Session
from ....db.session import get_db
from pydantic import BaseModel
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)

router = APIRouter()

# These endpoints checks for superuser values in database.

@router.get("/users", response_model=List[UserPublic])
def list_all_users(db: Session = Depends(get_db), admin_user: User = Depends(get_current_super_user)):
    """
    Endpoint to list all users. Accessible only by Superuser.
    """
    users = get_all_users(db)
    # Assuming get_all_users returns a list of SQLAlchemy User models, 
    # convert them to a list of UserPublic models
    return [UserPublic.from_orm(user) for user in users]
    #return [UserPublic(id=user.id, username=user.username, email=user.email, first_name=user.first_name, last_name=user.last_name, is_active=user.is_active) for user in users]

@router.get("/is-superuser")
def is_admin(user: User = Depends(get_current_active_user)) -> dict:
    if not user.is_superuser:
        logger.info(f"User {user.username} attempted to access superuser endpoint but is not an superuser")
        raise HTTPException(status_code=403, detail="User does not have superuser privileges")
    
    logger.info(f"Superuser check successful for user: {user.username}")
    return {"message": f"User {user.username} is superuser"}

@router.patch("/soft-delete/{username}")
def soft_delete_user(username: str, db: Session = Depends(get_db), current_superuser: User = Depends(get_current_super_user)):
    if username == current_superuser.username:
        logger.warning(f"Superuser {current_superuser.username} attempted to soft-delete themselves")
        raise HTTPException(status_code=403, detail="Superuser users cannot soft-delete themselves")
    user = get_user_by_username(db, username=username, include_deleted=False)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_deleted = True
    db.add(user)
    db.commit()
    logger.info(f"User {username} soft-deleted by Superuser {current_superuser.username}")
    return {"message": f"User {username} has been soft-deleted"}

@router.patch("/make-superuser/{username}")
def make_user_admin(username: str, db: Session = Depends(get_db), current_superuser: User = Depends(get_current_super_user)):
    if username == current_superuser.username:
        logger.info(f"Superuser user {username} attempted to modify their own Superuser status")
        raise HTTPException(status_code=400, detail="Superuser users cannot modify their own Superuser status")

    user = get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_deleted:
        raise HTTPException(status_code=400, detail="Cannot modify a deleted user")

    user.is_superuser = True
    db.add(user)
    db.commit()
    logger.info(f"User {username} granted Superuser privileges by {current_superuser.username}")
    return {"message": f"User {username} has been granted Superuser privileges"}

@router.patch("/revoke-superuser/{username}")
def revoke_admin(username: str, db: Session = Depends(get_db), current_superuser: User = Depends(get_current_super_user)):
    if username == current_superuser.username:
        logger.info(f"Super user {username} attempted to revoke their own superuser status")
        raise HTTPException(status_code=400, detail="Super users cannot revoke their own superuser status")

    user = get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_deleted:
        raise HTTPException(status_code=400, detail="Cannot modify a deleted user")

    user.is_superuser = False
    db.add(user)
    db.commit()
    logger.info(f"Superuser privileges revoked from user {username} by Superuser {current_superuser.username}")
    return {"message": f"Superuser privileges have been revoked from user {username}"}

ALLOWED_ROLES = ['member', 'moderator', 'administrator']  # Define allowed roles

@router.patch("/update-role/{username}", response_model=UserPublic)
def update_user_role_endpoint(username: str, role_update: UserRoleUpdate, db: Session = Depends(get_db), current_super: User = Depends(get_current_super_user)):
    logger.info(f"Received request to update role for user {username} to {role_update.role}")

    if username == current_super.username:
        logger.warning(f"Superuser {username} attempted to modify their own role")
        return JSONResponse(status_code=400, content={"detail": "Superusers cannot modify their own role"})

    user = get_user_by_username(db, username=username)
    if not user:
        logger.error(f"User {username} not found for role update")
        return JSONResponse(status_code=404, content={"detail": "User not found"})

    logger.debug(f"Current role for user {username}: {user.role}")
    if user.role.lower() == role_update.role.lower():
        message = f"User {username} is already assigned the role '{role_update.role}'. No changes made."
        logger.info(message)
        return JSONResponse(status_code=200, content={"message": message})

    updated_user = update_user_role(db, user, role_update.role.capitalize())
    logger.info(f"User {username}'s role updated to {updated_user.role} by superuser {current_super.username}")

    return UserPublic.from_orm(updated_user)

