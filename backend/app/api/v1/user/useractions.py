from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
import logging
from ....db.session import get_db
from ....schemas.user import UserPublic, UserUpdate
from ....core.security import get_current_active_user
from ....models.user import User
from ....crud.crud_user import update_user_profile 

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.get("/profile", response_model=UserPublic)
def get_user_profile(current_user: User = Depends(get_current_active_user)):
    logger.info(f"Retrieving profile for user: {current_user.username}")
    return current_user

@router.patch("/profile", response_model=UserPublic)
def update_user_profile_partial(update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    logger.info(f"Updating profile for user: {current_user.username}")
    updated_user = update_user_profile(db, user_id=current_user.id, update_data=update_data)
    if not updated_user:
        logger.error(f"User not found for user ID: {current_user.id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Profile updated successfully for user: {current_user.username}")
    return updated_user