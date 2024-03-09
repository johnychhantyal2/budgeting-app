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

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase):
    TransactionID: int
    UserID: int

    class Config:
        orm_mode = True
