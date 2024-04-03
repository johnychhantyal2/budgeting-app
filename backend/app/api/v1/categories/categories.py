from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from ....db.session import get_db
from ....schemas.categories import CategoryCreate, Category, CategoryUpdate
from ....crud.crud_categories import create_category, get_category, get_user_categories, update_category, delete_category
from ....models.user import User
from ....core.security import get_current_active_user
from slowapi import Limiter
from slowapi.util import get_remote_address
from ....config import RATE_LIMITS

# Assuming you have the limiter instance set up as shown above
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/", response_model=Category)
@limiter.limit(RATE_LIMITS["write"])  # This limits to 5 requests per minute
async def create_category_endpoint(request: Request,category_data: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_category(db=db, category_data=category_data, user_id=current_user.id)

@router.get("/", response_model=List[Category])
@limiter.limit(RATE_LIMITS["read"])  # This limits to 5 requests per minute
async def read_categories(request: Request,db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_user_categories(db=db, user_id=current_user.id)

@router.get("/{category_id}/", response_model=Category)
@limiter.limit(RATE_LIMITS["read"])  # This limits to 5 requests per minute
async def read_category(request: Request,category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    category = get_category(db=db, category_id=category_id, user_id=current_user.id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}/", response_model=Category)
@limiter.limit(RATE_LIMITS["write"])  # This limits to 5 requests per minute
async def update_category_endpoint(request: Request,category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Call update_category, which now includes the unique name check
    updated_category = update_category(db=db, category_id=category_id, category_data=category_data, user_id=current_user.id)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found or you don't have permission to update it")
    return updated_category

@router.delete("/{category_id}/", response_model=dict)
@limiter.limit(RATE_LIMITS["default"])  # This limits to 5 requests per minute
async def delete_category_endpoint(request: Request,category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    success = delete_category(db=db, category_id=category_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found or you don't have permission to delete it")
    return {"message": "Category deleted successfully"}
