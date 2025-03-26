from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from app.repositories.product_repository import ProductRepository
from app.models.product_model import Product
from app.schemas.product_schema import (
    ProductResponse,
    ProductCreate,
    ProductUpdate,
    ProductUpdateStock,
)
from app.repositories.category_repository import CategoryRepository
import shutil
import os
from uuid import uuid4
from typing import Optional
from decimal import Decimal, ROUND_HALF_UP


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
    def get_product_by_id(db: Session, product_id: int) -> Product:
        product = ProductRepository.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        total_discount = sum(
            discount.discount_percentage for discount in product.discounts
        )

        discounted_price = product.price - (product.price * total_discount / 100)
        product.price = max(
            discounted_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), 
            Decimal("0.00")
        )

        return product

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())

        return ProductRepository.create_product(db, product)

    @staticmethod
    def save_image(image: Optional[UploadFile]) -> str:
        UPLOAD_DIR = "uploads/products"
        DEFAULT_IMAGE = "uploads/defaults/no_product_image.png"
        ALLOWED_TYPES = ["image/jpeg", "image/png"]

        if image and image.__class__.__name__ == "UploadFile" and image.filename:
            if image.content_type not in ALLOWED_TYPES:
                raise HTTPException(status_code=400, detail="Apenas arquivos JPG ou PNG são permitidos.")

            extension = image.filename.split(".")[-1]
            filename = f"{uuid4()}.{extension}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            os.makedirs(UPLOAD_DIR, exist_ok=True)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            image_path = f"/{file_path}"
        else:
            image_path = f"/{DEFAULT_IMAGE}"

        return image_path

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
