from sqlalchemy.orm import Session
from ..models.category import Category as CategoryModel
from ..schemas.categories import CategoryCreate, CategoryUpdate

# Create a new category
def create_category(db: Session, category_data: CategoryCreate, user_id: int):
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

# Update a category
def update_category(db: Session, category_id: int, category_data: CategoryUpdate, user_id: int):
    db_category = get_category(db, category_id, user_id)
    if db_category:
        update_data = category_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
        return db_category
    return None

# Delete a category
def delete_category(db: Session, category_id: int, user_id: int):
    db_category = get_category(db, category_id, user_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False
