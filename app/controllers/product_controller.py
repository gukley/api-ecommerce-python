from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductUpdateStock,
)
from app.services.product_service import ProductService
from app.dependencies.auth import is_moderator, is_admin

router = APIRouter()


@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return ProductService.get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    return ProductService.create_product(db, product_data)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    return ProductService.update_product(db, product_id, product_data)


@router.put("/{product_id}/stock", response_model=ProductResponse)
def update_stock(
    product_id: int,
    product_data: ProductUpdateStock,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    return ProductService.update_stock(db, product_id, product_data)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    ProductService.delete_product(db, product_id)
    return
