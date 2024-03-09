# app/crud/crud_user.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import get_password_hash
from datetime import datetime 

def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user in the database.
    """
    hashed_password = get_password_hash(user_in.password)  # Ensure you have a utility function to hash passwords
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        phone_number=user_in.phone_number,
        date_of_birth=user_in.date_of_birth,
        bio=user_in.bio,
        country=user_in.country,
        city=user_in.city,
        postal_code=user_in.postal_code,
        address_line=user_in.address_line,
        is_active=True,  # You might want to set this to False if email verification is required
        is_superuser=False,  # Default to False, can be changed manually or through another process
        date_joined=datetime.utcnow(),  # Set the current datetime
        # Include other fields as necessary
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")

def get_user_by_email(db: Session, email: str) -> User:
    """
    Retrieve a user by email address.
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str, include_deleted: bool = False) -> User:
    """
    Retrieve a user by username, with an option to include or exclude soft-deleted users.
    """
    query = db.query(User).filter(User.username == username)
    if not include_deleted:
        query = query.filter(User.is_deleted == False)
    return query.first()