# app/core/security.py

from datetime import datetime, timedelta
import os
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from ..crud import crud_user
from sqlalchemy.orm import Session
from ..models.user import User

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

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Create a JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default to short-lived token for security
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

