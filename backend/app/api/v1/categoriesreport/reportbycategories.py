from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ....db.session import get_db
from datetime import date, datetime, timedelta
from sqlalchemy import func
from typing import List
from ....schemas.reportbycategories import ExpensePercentageReport,ExpenseReportByCategory,BudgetOverview  # You need to define this schema
from ....core.security import get_current_active_user
from ....models.user import User
from ....models.transactions import Transaction
from ....models.category import Category

router = APIRouter()

@router.get("/categories/expenses/{year}/{month}", response_model=List[ExpenseReportByCategory])
def get_expenses_by_category(year: int, month: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1)  # Adjust for month/year differences

    expenses = db.query(
        Category.id.label("id"),
        Category.name.label("category_name"),
        func.sum(Transaction.Amount).label("total_amount")
    ).join(Category, Category.id == Transaction.CategoryID).filter(
        Transaction.Date >= start_date,
        Transaction.Date < end_date,
        Transaction.UserID == current_user.id,
        Transaction.Is_Income == False
    ).group_by(Category.id, Category.name).all()

    # Convert to ExpenseReportByCategory schema
    report = [ExpenseReportByCategory(id=expense.id, category_name=expense.category_name, total_amount=expense.total_amount) for expense in expenses]
    return report

@router.get("/categories/expense-percentages/{year}/{month}", response_model=List[ExpensePercentageReport])
def get_expense_percentages(year: int, month: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1)

    total_income = db.query(
        func.sum(Transaction.Amount)
    ).filter(
        Transaction.Date >= start_date,
        Transaction.Date < end_date,
        Transaction.UserID == current_user.id,
        Transaction.Is_Income == True
    ).scalar() or 0  # Default to 0 if no income

    expense_percentages = db.query(
        Category.id.label("id"),
        Category.name.label("category_name"),
        func.sum(Transaction.Amount).label("total_amount")
    ).join(Category, Category.id == Transaction.CategoryID).filter(
        Transaction.Date >= start_date,
        Transaction.Date < end_date,
        Transaction.UserID == current_user.id,
        Transaction.Is_Income == False
    ).group_by(Category.id, Category.name).all()

    # Convert to ExpensePercentageReport schema
    report = [
        ExpensePercentageReport(
            id=expense.id,
            category_name=expense.category_name,
            percentage=(expense.total_amount / total_income * 100) if total_income else 0
        ) for expense in expense_percentages
    ]
    return report

@router.get("/budgets/{year}/{month}/budget-overview", response_model=BudgetOverview)
def get_monthly_budget_overview(year: int, month: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1)  # Adjust for month/year differences

    # Calculate total income
    total_income = db.query(
        func.sum(Transaction.Amount)
    ).filter(
        Transaction.Date >= start_date,
        Transaction.Date < end_date,
        Transaction.UserID == current_user.id,
        Transaction.Is_Income == True
    ).scalar() or 0.0

    # Calculate total expenses
    total_expenses = db.query(
        func.sum(Transaction.Amount)
    ).filter(
        Transaction.Date >= start_date,
        Transaction.Date < end_date,
        Transaction.UserID == current_user.id,
        Transaction.Is_Income == False
    ).scalar() or 0.0

    # Compute balance
    balance = total_income - total_expenses

    return BudgetOverview(total_income=total_income, total_expenses=total_expenses, balance=balance)