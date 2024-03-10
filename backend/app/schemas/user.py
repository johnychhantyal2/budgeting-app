# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import date, datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    address_line: Optional[str] = Field(None, max_length=255)
    # Note: Fields like is_active, is_superuser, hashed_password, etc., are not included as they should not be directly provided by the user upon registration.

class UserLogin(BaseModel):
    username: str  # This could be an email or username depending on your login logic
    password: str

class UserPublic(BaseModel):
    # id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    role: str = "member"  # Default role
    bio: Optional[str] = None
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    address_line: Optional[str] = Field(None, max_length=255)
    last_login: Optional[datetime] = None
    # Include other fields that are safe to expose publicly
    # Do NOT include the password or any other sensitive information

    class Config:
        orm_mode = True
        from_attributes = True

class PasswordChange(BaseModel):
    old_password: str = Field(..., min_length=8, description="The current password of the user.")
    new_password: str = Field(..., min_length=8, description="The new password for the user.")

    class Config:
        orm_mode = True

class UserRoleUpdate(BaseModel):
    role: str = Field(..., description="The new role for the user.")

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    country: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    address_line: Optional[str] = Field(None, max_length=255)

    class Config:
        orm_mode = True
        extra = "forbid" # Forbid any extra fields not defined in the model

# Optional: Custom validator example
@validator('*')
def check_empty_strings(cls, value, field):
    if value == "":
        raise ValueError(f"{field.name} cannot be empty")
    return value