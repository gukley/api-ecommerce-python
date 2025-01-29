from sqlalchemy.orm import Session
from app.repositories.category_repository import CategoryRepository
from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


class CategoryService:
    @staticmethod
    def get_all_categories(db: Session) -> list[Category]:
        return CategoryRepository.get_all_categories(db)

    @staticmethod
    def get_categorie_by_id(db: Session, category_id: int) -> Category:
        return CategoryRepository.get_categories_by_id(db, category_id)

    @staticmethod
    def create_category(db: Session, category_data: CategoryCreate) -> Category:
        category = Category(**category_data.dict())
        return CategoryRepository.create_category(db, category)

    @staticmethod
    def update_category(
        db: Session, category_id: int, category_data: CategoryUpdate
    ) -> Category:
        updates = category_data.dict(exclude_unset=True)
        return CategoryRepository.update_category(db, category_id, updates)

    @staticmethod
    def delete_category(db: Session, category_id: int):
        CategoryRepository.delete_category(db, category_id)
