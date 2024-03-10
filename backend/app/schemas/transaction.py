# app/schemas/transaction.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

class TransactionBase(BaseModel):
    Amount: float
    Date: date
    Description: Optional[str] = None
    Note: Optional[str] = None
    Location: Optional[str] = None
    CategoryID: Optional[int] = None
    Is_Income: bool = False  # Add this line

class TransactionCreate(TransactionBase):
    # For creating a transaction, all fields except IsIncome should be required
    Amount: float
    Date: date

class TransactionUpdate(BaseModel):
    # All fields are optional for updates
    Amount: Optional[float] = None
    Date: Optional[date] = None
    Description: Optional[str] = None
    Note: Optional[str] = None
    Location: Optional[str] = None
    CategoryID: Optional[int] = None
    Is_Income: Optional[bool] = None  # Ensure this is included for income/expense updates

class Transaction(TransactionBase):
    TransactionID: int
    UserID: int

    class Config:
        orm_mode = True
