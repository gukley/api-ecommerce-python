from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
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
from typing import Optional, Union
from app.repositories.category_repository import CategoryRepository

router = APIRouter()


@router.get(
    "/",
    response_model=list[ProductResponse],
    summary="Obter todos os produtos",
    description="Retorna uma lista contendo todos os produtos cadastrados no sistema.",
)
def get_products(db: Session = Depends(get_db)):
    return ProductService.get_all_products(db)


@router.get(
    "/user/{user_id}",
    response_model=list[ProductResponse],
    summary="Obter produtos por usuário",
    description="Retorna uma lista de produtos cadastrados por um usuário específico.",
)
def get_products_by_user(user_id: int, db: Session = Depends(get_db)):
    return ProductService.get_all_products_by_user(db, user_id)


@router.get(
    "/category/{category_id}",
    response_model=list[ProductResponse],
    summary="Obter produtos por categoria",
    description="Retorna uma lista de produtos pertencentes a uma categoria específica.",
)
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    return ProductService.get_product_by_category(db, category_id)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Obter um produto específico",
    description="Retorna detalhes de um produto específico com base no seu ID.",
    responses={404: {"description": "Produto não encontrado"}},
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo produto",
    description="Cria um novo produto. Requer privilégios de moderador.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def create_product(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    category_id: int = Form(...),
    image: Optional[Union[UploadFile, str]] = File(None),
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    category = CategoryRepository.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product_data = ProductCreate(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id,
        image_path = ProductService.save_image(image)
    )

    return ProductService.create_product(db, product_data)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Atualizar um produto",
    description="Atualiza informações gerais de um produto específico com base no seu ID. Requer privilégios de moderador.",
    responses={
        404: {"description": "Produto não encontrado"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    return ProductService.update_product(db, product_id, product_data)


@router.put(
    "/{product_id}/stock",
    response_model=ProductResponse,
    summary="Atualizar estoque de um produto",
    description="Atualiza o estoque de um produto específico. Requer privilégios de moderador.",
    responses={
        404: {"description": "Produto não encontrado"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def update_stock(
    product_id: int,
    product_data: ProductUpdateStock,
    db: Session = Depends(get_db),
    _: dict = Depends(is_moderator),
):
    return ProductService.update_stock(db, product_id, product_data)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir um produto",
    description="Exclui um produto específico com base no seu ID. Requer privilégios de administrador.",
    responses={
        404: {"description": "Produto não encontrado"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    ProductService.delete_product(db, product_id)
