# app/api/v1/routes.py

from fastapi import APIRouter
from .endpoints import auth
from .admin import admin_user_operations # Import admin routes from admin_user_operations.py

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(admin_user_operations.router, prefix="/admin", tags=["Admin"])  # Include admin routes