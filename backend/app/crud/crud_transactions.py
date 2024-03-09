# app/crud/crud_transaction.py

from sqlalchemy.orm import Session
from ..schemas.transaction import TransactionCreate
from ..models.transactions import Transaction

 # Adjust the import path as necessary

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(**transaction.dict(), UserID=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Transaction).filter(Transaction.UserID == user_id).offset(skip).limit(limit).all()

def update_transaction(db: Session, transaction_id: int, transaction_data: TransactionCreate, user_id: int):
    db_transaction = db.query(Transaction).filter(
        Transaction.TransactionID == transaction_id, Transaction.UserID == user_id
    ).first()
    if db_transaction:
        update_data = transaction_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    return None

# In your CRUD operations (crud_transactions.py)
def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db_transaction = db.query(Transaction).filter(
        Transaction.TransactionID == transaction_id, 
        Transaction.UserID == user_id
    ).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return True
    return False

# In crud_transactions.py
def get_transaction(db: Session, transaction_id: int, user_id: int):
    return db.query(Transaction).filter(Transaction.TransactionID == transaction_id, Transaction.UserID == user_id).first()



# Implement additional CRUD functions as needed (e.g., get_transaction, update_transaction, delete_transaction)
