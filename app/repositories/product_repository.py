from sqlalchemy.orm import Session
from app.models.product_model import Product
from sqlalchemy.orm import joinedload


class ProductRepository:
    @staticmethod
    def get_all_products(db: Session) -> list[Product]:
        return db.query(Product).options(joinedload(Product.discounts)).all()

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
        if product:
            db.delete(product)
            db.commit()
