from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductUpdateStock


class ProductService:
    @staticmethod
    def get_all_products(db: Session) -> list[Product]:
        return ProductRepository.get_all_products(db)

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        return ProductRepository.get_product_by_id(db, product_id)

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        return ProductRepository.create_product(db, product)

    @staticmethod
    def update_product(
        db: Session, product_id: int, product_data: ProductUpdate
    ) -> Product:
        updates = product_data.model_dump(exclude_unset=True)
        return ProductRepository.update_product(db, product_id, updates)

    @staticmethod
    def update_stock(
        db: Session, product_id: int, new_stock: ProductUpdateStock
    ) -> Product:
        updates = new_stock.model_dump(exclude_unset=True)
        return ProductRepository.update_stock(db, product_id, updates)

    @staticmethod
    def delete_product(db: Session, product_id: int):
        ProductRepository.delete_product(db, product_id)
