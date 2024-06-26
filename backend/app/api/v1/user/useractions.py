from fastapi import APIRouter, Depends,HTTPException, Request
from sqlalchemy.orm import Session
import logging
from ....db.session import get_db
from ....schemas.user import UserPublic, UserUpdate
from ....core.security import get_current_active_user
from ....models.user import User
from ....crud.crud_user import update_user_profile
from slowapi import Limiter
from slowapi.util import get_remote_address
from ....config import RATE_LIMITS

# Assuming you have the limiter instance set up as shown above
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.get("/profile", response_model=UserPublic)
@limiter.limit(RATE_LIMITS["read"])  # This limits to 10 requests per minute
def get_user_profile(request: Request,current_user: User = Depends(get_current_active_user)):
    logger.info(f"Retrieving profile for user: {current_user.username}")
    return current_user

@router.patch("/profile", response_model=UserPublic)
@limiter.limit(RATE_LIMITS["write"])  # This limits to 3 requests per minute
def update_user_profile_partial(request: Request,update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    logger.info(f"Updating profile for user: {current_user.username}")
    updated_user = update_user_profile(db, user_id=current_user.id, update_data=update_data)
    if not updated_user:
        logger.error(f"User not found for user ID: {current_user.id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Profile updated successfully for user: {current_user.username}")
    return updated_user