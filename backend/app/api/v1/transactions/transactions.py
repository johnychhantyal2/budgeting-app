# app/api/endpoints/transaction.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....db.session import get_db
from ....schemas.transaction import TransactionCreate, Transaction
from ....schemas.transaction import Transaction as TransactionSchema
from ....models.transactions import Transaction as SQLAlchemyTransaction
from ....crud.crud_transactions import create_transaction, get_transactions, update_transaction, delete_transaction, get_transaction
from ....models.user import User
from ....core.security import get_current_active_user
# Import other CRUD functions as necessary

router = APIRouter()

@router.post("/", response_model=Transaction)
async def create_transaction_endpoint(transaction: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_transaction(db=db, transaction=transaction, user_id=current_user.id)

@router.get("/", response_model=List[Transaction])
async def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    transactions = get_transactions(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return transactions

@router.get("/{transaction_id}/", response_model=Transaction)
async def read_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    transaction = get_transaction(db=db, transaction_id=transaction_id, user_id=current_user.id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}/", response_model=Transaction)
async def update_transaction_endpoint(
    transaction_id: int, transaction_data: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    updated_transaction = update_transaction(
        db=db, transaction_id=transaction_id, transaction_data=transaction_data, user_id=current_user.id
    )
    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found or you don't have permission to update it")
    return updated_transaction

@router.delete("/{transaction_id}/", response_model=dict)
async def delete_transaction_endpoint(
    transaction_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    success = delete_transaction(
        db=db, 
        transaction_id=transaction_id, 
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found or you don't have permission to delete it")
    return {"message": "Transaction deleted successfully"}

@router.get("/recent", response_model=List[TransactionSchema])
def get_recent_transactions(limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    transactions = db.query(SQLAlchemyTransaction).filter(SQLAlchemyTransaction.UserID == current_user.id).order_by(SQLAlchemyTransaction.Date.desc()).limit(limit).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return transactions

# Add endpoints for updating and deleting transactions as needed
