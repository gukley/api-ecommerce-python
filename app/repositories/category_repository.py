from sqlalchemy.orm import Session
from app.models.category_model import Category


class CategoryRepository:
    @staticmethod
    def get_all_categories(db: Session) -> list[Category]:
        return db.query(Category).all()

    @staticmethod
    def get_all_categories_by_user(db: Session, user_id: int) -> list[Category]:
        return db.query(Category).filter(Category.user_id == user_id).all()

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Category:
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def create_category(db: Session, category: Category) -> Category:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def update_category(db: Session, category_id: int, updates: dict) -> Category:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            for key, value in updates.items():
                setattr(category, key, value)
            db.commit()
            db.refresh(category)
        return category

    @staticmethod
    def delete_category(db: Session, category_id: int):
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            db.delete(category)
            db.commit()

    @staticmethod
    def update_category_image(db: Session, category_id: int, image_path: str) -> Category:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            category.image_path = image_path
            db.commit()
            db.refresh(category)
        return category
