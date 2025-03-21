from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.product_repository import ProductRepository
from app.models.product_model import Product
from app.schemas.product_schema import (
    ProductResponse,
    ProductCreate,
    ProductUpdate,
    ProductUpdateStock,
)
from app.repositories.category_repository import CategoryRepository


class ProductService:
    @staticmethod
    def get_all_products(db: Session) -> list[Product]:
        return ProductRepository.get_all_products(db)

    @staticmethod
    def get_all_products_by_user(db: Session, user_id: int) -> list[Product]:
        return ProductRepository.get_all_products_by_user(db, user_id)

    @staticmethod
    def get_product_by_category(db: Session, category_id: int) -> list[Product]:
        return ProductRepository.get_product_by_category(db, category_id)

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> ProductResponse:
        product = ProductRepository.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        total_discount = sum(
            discount.discount_percentage for discount in product.discounts
        )

        discounted_price = max(
            product.price - (product.price * total_discount / 100), 0
        )

        return ProductResponse(
            id=product.id,
            category=product.category,
            name=product.name,
            price=product.price - discounted_price,
            stock=product.stock,
            discounts=product.discounts,
        )

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())

        category = CategoryRepository.get_category_by_id(db, product.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        return ProductRepository.create_product(db, product)

    @staticmethod
    def update_product(
        db: Session, product_id: int, product_data: ProductUpdate
    ) -> Product:
        updates = product_data.model_dump(exclude_unset=True)

        category = CategoryRepository.get_category_by_id(db, product_data.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        product = ProductRepository.update_product(db, product_id, updates)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    @staticmethod
    def update_stock(
        db: Session, product_id: int, new_stock: ProductUpdateStock
    ) -> Product:
        updates = new_stock.model_dump(exclude_unset=True)
        product = ProductRepository.update_stock(db, product_id, updates["stock"])
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    @staticmethod
    def delete_product(db: Session, product_id: int):
        ProductRepository.delete_product(db, product_id)
