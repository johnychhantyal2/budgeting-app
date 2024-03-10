# app/api/v1/routes.py

from fastapi import APIRouter
from .endpoints import auth
from .admin import admin_user_operations # Import admin routes from admin_user_operations.py
from .transactions import transactions # Import transactions routes from transactions.py
from .categories import categories # Import categories routes from categories.py
from .categoriesreport import reportbycategories # Import categories report routes from reportbycategories.py
from .user import useractions # Import user routes from useractions.py

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(admin_user_operations.router, prefix="/admin", tags=["Admin"])  # Include admin routes
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])  # Include transactions routes
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])  # Include Categories routes
api_router.include_router(reportbycategories.router, prefix="/reports", tags=["Reports"])  # Include Report routes
api_router.include_router(useractions.router, prefix="/user", tags=["UserActions"])  # Include Report routes