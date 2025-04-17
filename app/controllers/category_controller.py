from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate, CategoryImageUpdate
from app.services.category_service import CategoryService
from app.models.user_model import User
from app.dependencies.auth import is_admin
from app.dependencies.category_form import category_create_form, category_update_form


router = APIRouter()


@router.get(
    "/",
    response_model=list[CategoryResponse],
    summary="Obter todas as categorias",
    description="Retorna uma lista contendo todas as categorias cadastradas no sistema.",
)
def get_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all_categories(db)


@router.get(
    "/user/{user_id}",
    response_model=list[CategoryResponse],
    summary="Obter todas as categorias com base em um admin",
    description="Retorna uma lista contendo todas as categorias cadastradas por um admin especifico no sistema.",
)
def get_categories(user_id: int, db: Session = Depends(get_db)):
    return CategoryService.get_all_categories_by_user(db, user_id)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Obter uma categoria específica",
    description="Retorna detalhes de uma categoria específica com base no seu ID.",
    responses={404: {"description": "Categoria não encontrada."}},
)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = CategoryService.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova categoria",
    description="Cria uma nova categoria. Requer privilégios de administrador.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def create_category(
    category_data: CategoryCreate = Depends(category_create_form),
    db: Session = Depends(get_db),
    user: User = Depends(is_admin),
):
    return CategoryService.create_category(db, category_data, user)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Atualizar uma categoria existente",
    description="Atualiza os detalhes de uma categoria específica com base no seu ID. Requer privilégios de administrador.",
    responses={
        404: {"description": "Categoria não encontrada"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin),
):
    updated_category = CategoryService.update_category(db, category_id, category_data)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return updated_category


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir uma categoria",
    description="Exclui uma categoria específica com base no seu ID. Requer privilégios de administrador.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def delete_category(
    category_id: int, db: Session = Depends(get_db), _: User = Depends(is_admin)
):
    CategoryService.delete_category(db, category_id)
    return

@router.put(
    "/{category_id}/image",
    response_model=CategoryResponse,
    summary="Atualizar imagem da categoria",
    description="Atualiza a imagem da categoria. Requer privilégios de administrador.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def update_user_image(
    category_id: int,
    category_image: CategoryImageUpdate = Depends(category_update_form),
    db: Session = Depends(get_db),
    _: User = Depends(is_admin),
):
    return CategoryService.update_category_image(db, category_id, category_image)
