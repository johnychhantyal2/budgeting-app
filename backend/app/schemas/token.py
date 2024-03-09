# app/schemas/token.py

from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = Field(None, description="A unique identifier for the user")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"