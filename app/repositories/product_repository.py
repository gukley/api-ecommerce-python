from sqlalchemy.orm import Session
from app.models.product_model import Product
from sqlalchemy.orm import joinedload
from fastapi import HTTPException


class ProductRepository:
    @staticmethod
    def get_all_products(db: Session) -> list[Product]:
        return db.query(Product).options(joinedload(Product.discounts)).all()

    @staticmethod
    def get_all_products_by_user(db: Session, user_id: int) -> list[Product]:
        return (
            db.query(Product)
            .join(Product.category)
            .options(joinedload(Product.discounts), joinedload(Product.category))
            .filter(Product.category.has(user_id=user_id))
            .all()
        )

    @staticmethod
    def get_product_by_category(db: Session, category_id: int) -> list[Product]:
        return (
            db.query(Product)
            .options(joinedload(Product.discounts))
            .filter(Product.category_id == category_id)
            .all()
        )

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        return (
            db.query(Product)
            .options(joinedload(Product.discounts))
            .filter(Product.id == product_id)
            .first()
        )

    @staticmethod
    def create_product(db: Session, product: Product) -> Product:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update_stock(db: Session, product_id: int, new_stock: int) -> Product:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.stock = new_stock
            db.commit()
            db.refresh(product)
        return product

    @staticmethod
    def update_product(db: Session, product_id: int, updates: dict) -> Product:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            for key, value in updates.items():
                setattr(product, key, value)
            db.commit()
            db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()

        if product.order_items and len(product.order_items) > 0:
            raise HTTPException(404, "Product has orders")

        if product:
            db.delete(product)
            db.commit()
