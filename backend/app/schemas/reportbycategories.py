from pydantic import BaseModel

class ExpenseReportByCategory(BaseModel):
    id: int
    category_name: str  # Optional, depending on whether you want to include the category name in the report
    total_amount: float

    class Config:
        orm_mode = True

class ExpensePercentageReport(BaseModel):
    id: int
    category_name: str  # Optional
    percentage: float

    class Config:
        orm_mode = True

class BudgetOverview(BaseModel):
    total_income: float
    total_expenses: float
    balance: float