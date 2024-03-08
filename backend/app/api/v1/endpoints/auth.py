from fastapi import APIRouter, Depends, HTTPException, status, Request  # Include Request
from sqlalchemy.orm import Session
from typing import Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Include this import
import json
from ....crud import crud_user
from ....db.session import get_db
from ....schemas.user import UserCreate, UserPublic, UserLogin  # Make sure to use UserPublic
from ....core.security import authenticate_user, create_access_token
from ....schemas.token import Token
from datetime import timedelta
from ....core.config import settings  # Import settings

router = APIRouter()

@router.post("/register", response_model=UserPublic)  # Use UserPublic here
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    # Check if the username or email already exists
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    user = crud_user.create_user(db=db, user_in=user_in)
    return user  # Ensure the returned user matches the UserPublic schema

@router.post("/login", response_model=Token)
async def login(request: Request, db: Session = Depends(get_db)) -> Any:
    data = await request.body()
    data_dict = json.loads(data.decode())
    username = data_dict.get("username")
    password = data_dict.get("password")
    
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}