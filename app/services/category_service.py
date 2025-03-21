from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.category_repository import CategoryRepository
from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.models.user_model import User


class CategoryService:
    @staticmethod
    def get_all_categories(db: Session) -> list[Category]:
        return CategoryRepository.get_all_categories(db)

    @staticmethod
    def get_all_categories_by_user(db: Session, user_id: int) -> list[Category]:
        return CategoryRepository.get_all_categories_by_user(db, user_id)

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Category:
        return CategoryRepository.get_category_by_id(db, category_id)

    @staticmethod
    def create_category(
        db: Session, category_data: CategoryCreate, current_user: User
    ) -> Category:
        category = Category(**category_data.model_dump())
        category.user_id = current_user.id
        return CategoryRepository.create_category(db, category)

    @staticmethod
    def update_category(
        db: Session, category_id: int, category_data: CategoryUpdate
    ) -> Category:
        updates = category_data.model_dump(exclude_unset=True)
        category = CategoryRepository.update_category(db, category_id, updates)

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        return category

    @staticmethod
    def delete_category(db: Session, category_id: int):
        CategoryRepository.delete_category(db, category_id)
