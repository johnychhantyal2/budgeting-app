from sqlalchemy.orm import Session
from ..models.category import Category as CategoryModel
from ..schemas.categories import CategoryCreate, CategoryUpdate
from fastapi import HTTPException

def create_category(db: Session, category_data: CategoryCreate, user_id: int):
    # Check if the category name already exists for the user
    existing_category = db.query(CategoryModel).filter(CategoryModel.name == category_data.name, CategoryModel.user_id == user_id).first()
    if existing_category:
        # If a category with the same name exists, raise an HTTPException
        raise HTTPException(status_code=400, detail=f"Category '{category_data.name}' already exists.")

    # Proceed with creating the new category if the name is unique for the user
    db_category = CategoryModel(**category_data.dict(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Get a single category by ID
def get_category(db: Session, category_id: int, user_id: int):
    return db.query(CategoryModel).filter(CategoryModel.id == category_id, CategoryModel.user_id == user_id).first()

# Get all categories for a user
def get_user_categories(db: Session, user_id: int):
    return db.query(CategoryModel).filter(CategoryModel.user_id == user_id).all()

# Update a category with a check to avoid updating to an existing name
def update_category(db: Session, category_id: int, category_data: CategoryUpdate, user_id: int):
    db_category = get_category(db, category_id, user_id)
    if not db_category:
        return None  # The category does not exist
    
    update_data = category_data.dict(exclude_unset=True)

    # If 'name' is in the update data, check if it's different and unique
    if 'name' in update_data and update_data['name'] != db_category.name:
        existing_category = db.query(CategoryModel).filter(
            CategoryModel.user_id == user_id,
            CategoryModel.name == update_data['name'],
            CategoryModel.id != category_id  # Exclude the current category from the check
        ).first()
        if existing_category:
            raise HTTPException(status_code=400, detail=f"Category '{update_data['name']}' already exists.")

    # Proceed with updating if the name is unique or unchanged
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

# Delete a category
def delete_category(db: Session, category_id: int, user_id: int):
    db_category = get_category(db, category_id, user_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False
