# app/crud/crud_admin.py

from sqlalchemy.orm import Session
from ..models.user import User  # Adjust the import path as necessary
from typing import List
from ..schemas.user import UserPublic

def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()

def update_user_role(db: Session, user: User, new_role: str) -> User:
    user.role = new_role
    db.add(user)
    db.commit()
    db.refresh(user)
    return user