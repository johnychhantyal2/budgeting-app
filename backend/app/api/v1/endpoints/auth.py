from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Any
from fastapi.security import OAuth2PasswordRequestForm
from ....crud import crud_user
from ....db.session import get_db
from ....schemas.user import UserCreate, UserPublic, PasswordChange,UserLogin
from ....core.security import authenticate_user, create_access_token, validate_password, get_password_hash, verify_password, add_token_to_blocklist, get_current_active_user, oauth2_scheme, validate_refresh_token
from ....schemas.token import Token
from datetime import timedelta
from ....core.config import settings
from ....models.user import User
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from ....config import RATE_LIMITS

# Configure logging
logger = logging.getLogger(__name__)

# Assuming you have the limiter instance set up as shown above
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/login", response_model=Token)  # Update Token model to include refresh_token
@limiter.limit(RATE_LIMITS["write"])  # This limits to 5 requests per minute
async def login(request: Request, user_login: UserLogin, db: Session = Depends(get_db)) -> Any:
    user = authenticate_user(db, user_login.username, user_login.password)
    if not user:
        logger.warning(f"Authentication failed for user: {user_login.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    tokens = create_access_token(
        username=user.username,
        access_token_expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_token_expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)  # Make sure to define this in your settings
    )
    logger.info(f"User {user_login.username} authenticated successfully")
    return tokens

@router.post("/register", response_model=UserPublic)  # Use UserPublic here
@limiter.limit(RATE_LIMITS["write"])  # This limits to 5 requests per minute
def register(request: Request, user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    # Check if the username or email already exists
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Validate the password
    if not validate_password(user_in.password):
        raise HTTPException(
            status_code=400,
            detail="Password does not meet security requirements.",
        )

    # Proceed with user creation, assuming create_user hashes the password
    user = crud_user.create_user(db=db, user_in=user_in)
    return user  # Ensure the returned user matches the UserPublic schema

@router.post("/change-password")
@limiter.limit(RATE_LIMITS["write"])  # This limits to 5 requests per minute
def change_password(request: Request, password_change: PasswordChange, user: User = Depends(get_current_active_user), db: Session = Depends(get_db)) -> Any:
    if not verify_password(password_change.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password.")
    if not validate_password(password_change.new_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password does not meet security requirements.")
    user.hashed_password = get_password_hash(password_change.new_password)
    db.commit()
    return {"message": "Password changed successfully."}

@router.post("/logout")
@limiter.limit(RATE_LIMITS["write"])  # This limits to 5 requests per minute
def logout(request: Request,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Any:
    is_added_to_blocklist = add_token_to_blocklist(db, token)
    if not is_added_to_blocklist:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not process logout request.")
    return {"message": "Logged out successfully."}

@router.post("/refresh-token", response_model=Token)
@limiter.limit(RATE_LIMITS["write"])  # This limits to 5 requests per minute
def refresh_token(request: Request,refresh_token: str, db: Session = Depends(get_db)) -> Any:
    username = validate_refresh_token(refresh_token, db)  # Implement this function to validate the refresh token and get the username
    if not username:
        logger.error("Invalid or expired refresh token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    tokens = create_access_token(username=username)
    logger.info(f"Access token refreshed successfully for user: {username}")
    return tokens
