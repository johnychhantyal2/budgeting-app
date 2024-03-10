from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....db.session import get_db
from ....schemas.categories import CategoryCreate, Category, CategoryUpdate
from ....crud.crud_categories import create_category, get_category, get_user_categories, update_category, delete_category
from ....models.user import User
from ....core.security import get_current_active_user

router = APIRouter()

@router.post("/", response_model=Category)
async def create_category_endpoint(category_data: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_category(db=db, category_data=category_data, user_id=current_user.id)

@router.get("/", response_model=List[Category])
async def read_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_user_categories(db=db, user_id=current_user.id)

@router.get("/{category_id}/", response_model=Category)
async def read_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    category = get_category(db=db, category_id=category_id, user_id=current_user.id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}/", response_model=Category)
async def update_category_endpoint(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Call update_category, which now includes the unique name check
    updated_category = update_category(db=db, category_id=category_id, category_data=category_data, user_id=current_user.id)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found or you don't have permission to update it")
    return updated_category

@router.delete("/{category_id}/", response_model=dict)
async def delete_category_endpoint(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    success = delete_category(db=db, category_id=category_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found or you don't have permission to delete it")
    return {"message": "Category deleted successfully"}
