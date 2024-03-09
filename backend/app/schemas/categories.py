from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for category creation
class CategoryCreate(BaseModel):
    name: str
    budgeted_amount: float
    color_code: Optional[str] = None

# Schema for category update
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    budgeted_amount: Optional[float] = None
    color_code: Optional[str] = None

# Schema for category response
class Category(BaseModel):
    id: int
    name: str
    budgeted_amount: float
    color_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
