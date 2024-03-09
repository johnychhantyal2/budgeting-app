# app/core/security.py

from datetime import datetime, timedelta
import os
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from ..crud import crud_user
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.token import TokenData
from ..models.blocklist import BlocklistedToken
import logging
from ..db.session import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Adjust "tokenUrl" based on your login endpoint
SECRET_KEY = settings.SECRET_KEY  # Define this in your settings, e.g., using environment variables
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # or whatever suits your application

def validate_password(plain_password: str) -> bool:
    # Check if password meets minimum length requirement
    if len(plain_password) < 8:
        return False
    
    # Check for additional strict requirements
    has_uppercase = any(char.isupper() for char in plain_password)
    has_lowercase = any(char.islower() for char in plain_password)
    has_digit = any(char.isdigit() for char in plain_password)
    has_special = any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?`~' for char in plain_password)
    
    return has_uppercase and has_lowercase and has_digit and has_special

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password.
    """
    return pwd_context.hash(password)

def create_access_token(username: str, access_token_expires_delta: Union[timedelta, None] = None, refresh_token_expires_delta: Union[timedelta, None] = None) -> dict:
    """
    Create JWT access and refresh tokens using the username as the subject of the tokens.
    """
    access_token_to_encode = {"sub": username}
    refresh_token_to_encode = {"sub": username}

    if access_token_expires_delta:
        access_expire = datetime.utcnow() + access_token_expires_delta
    else:
        access_expire = datetime.utcnow() + timedelta(minutes=15)  # Default to short-lived token for security
    
    if refresh_token_expires_delta:
        refresh_expire = datetime.utcnow() + refresh_token_expires_delta
    else:
        refresh_expire = datetime.utcnow() + timedelta(days=7)  # Default to a longer-lived refresh token

    access_token_to_encode.update({"exp": access_expire})
    refresh_token_to_encode.update({"exp": refresh_expire})

    access_token = jwt.encode(access_token_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    refresh_token = jwt.encode(refresh_token_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    logger.info(f"Tokens created for user: {username}")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def verify_token(token: str, credentials_exception) -> Union[str, Any]:
    """
    Verify a JWT token and return the payload if valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = crud_user.get_user_by_username(db, username)  # Assuming you have a function to fetch user by username
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    # Update last_login field
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    return user

async def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    from ..crud.crud_user import get_user_by_username  # Import the necessary function

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.error("JWT 'sub' claim is missing")
            raise credentials_exception
        logger.info(f"Token decoded successfully for username: {username}")
    except JWTError as e:
        logger.error(f"JWTError occurred: {e}")
        raise credentials_exception

    user = get_user_by_username(db, username=username)
    if user is None:
        logger.error(f"User not found for username: {username}")
        raise credentials_exception

    logger.info(f"User {username} authenticated successfully")
    return user

def add_token_to_blocklist(db: Session, token: str) -> bool:
    try:
        # Decode the token to get its expiry time
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        expires_at = datetime.utcfromtimestamp(payload.get("exp"))

        # Create a new BlocklistedToken instance
        blocklisted_token = BlocklistedToken(token=token, expires_at=expires_at)

        # Add to the database and commit
        db.add(blocklisted_token)
        db.commit()

        logger.info("Token successfully added to blocklist.")
        return True
    except JWTError as e:
        logger.error(f"JWT error adding token to blocklist: {e}")
        return False
    except Exception as e:
        logger.error(f"Error adding token to blocklist: {e}")
        return False
    
def validate_refresh_token(token: str, db: Session) -> str:
    try:
        # Decode the refresh token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        expiration: int = payload.get("exp")

        # Check if the token has expired
        if datetime.utcfromtimestamp(expiration) < datetime.utcnow():
            logger.error(f"Refresh token expired for user: {username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

        # Check if the token is in the blocklist (revoked)
        if db.query(BlocklistedToken).filter(BlocklistedToken.token == token).first():
            logger.error(f"Refresh token revoked for user: {username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")

    except JWTError as e:
        logger.error(f"JWT error validating refresh token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    return username