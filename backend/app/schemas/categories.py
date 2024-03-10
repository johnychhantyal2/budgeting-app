from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for category creation
class CategoryCreate(BaseModel):
    name: str
    budgeted_amount: float = Field(default=0.00)
    color_code: Optional[str] = None
    budgeted_limit: float = Field(default=0.00)
    description: Optional[str] = None
    #is_active: bool = Field(default=True)
    icon: Optional[str] = None

# Schema for category update
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    budgeted_amount: Optional[float] = None
    color_code: Optional[str] = None
    budgeted_limit: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    icon: Optional[str] = None

# Schema for category response
class Category(BaseModel):
    id: int
    name: str
    budgeted_amount: float
    budgeted_limit: Optional[float] = None  # new field added
    color_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    description: Optional[str]
    is_active: bool
    icon: Optional[str]

    class Config:
        orm_mode = True
