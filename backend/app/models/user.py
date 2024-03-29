# app/models/user.py

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Date, Enum
from sqlalchemy.orm import relationship
from ..db.session import Base
from ..models.category import Category # Used by SQLAlchemy relationship, not directly accessed
from ..models.transactions import Transaction # Used by SQLAlchemy relationship, not directly accessed

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, index=True)
    last_login = Column(DateTime, index=True)
    profile_picture = Column(String(255))  # Consider storing the picture itself in a static file server or a blob storage, and save the URL or path here
    phone_number = Column(String(20), index=True)
    date_of_birth = Column(Date)
    bio = Column(Text)
    country = Column(String(100), index=True)
    city = Column(String(100), index=True)
    postal_code = Column(String(20), index=True)
    address_line = Column(String(255))
    reset_password_token = Column(String(255), index=True)
    reset_password_token_expiry = Column(DateTime)
    email_verification_token = Column(String(255), index=True)
    is_email_verified = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    role = Column(Enum('member', 'moderator', 'administrator'), default='member', nullable=False)

    # Relationship to Categories
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")

     # Relationship to Transactions
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")


    # If you have relationships to other tables, define them here
    # For example, if users can have multiple posts:
    # posts = relationship("Post", back_populates="owner")
