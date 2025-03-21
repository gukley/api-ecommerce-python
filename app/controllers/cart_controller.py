from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cart_schema import CartResponse, CartItemsResponse
from app.services.cart_service import CartService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User
from app.schemas.cart_item_schema import (
    CartItemCreate,
    CartItemRemove,
    CartItemUpdate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=CartResponse,
    summary="Obter o carrinho do usuário",
    description="Retorna o carrinho atual do usuário autenticado.",
)
def get_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return CartService.get_cart_by_user(db, current_user)


@router.get(
    "/items",
    response_model=CartItemsResponse,
    summary="Obter itens do carrinho",
    description="Retorna todos os itens presentes no carrinho do usuário autenticado.",
)
def get_cart_items(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return CartService.get_cart_items(db, current_user)


@router.post(
    "/items",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Adicionar item ao carrinho",
    description="Adiciona um novo item ao carrinho do usuário autenticado.",
)
def add_item_to_cart(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    CartService.add_item_to_cart(db, cart_item, current_user)
    return


@router.post(
    "/",
    response_model=CartResponse,
    summary="Criar um carrinho",
    description="Cria um novo carrinho para o usuário autenticado caso ainda não exista.",
)
def create_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CartService.create_cart(db, current_user)


@router.delete(
    "/items",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover item do carrinho",
    description="Remove um item específico do carrinho do usuário autenticado.",
)
def remove_item_from_cart(
    cart_item: CartItemRemove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    CartService.remove_item_from_cart(db, cart_item, current_user)
    return


@router.delete(
    "/clear",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Limpar carrinho",
    description="Remove todos os itens do carrinho do usuário autenticado.",
)
def clear_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    CartService.clear_cart(db, current_user)
    return


@router.put(
    "/items",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Atualizar quantidade de item no carrinho",
    description="Atualiza a quantidade de um item específico no carrinho do usuário autenticado.",
)
def update_cart_items(
    cart_item: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    CartService.update_item_quantity(db, cart_item, current_user)
    return
