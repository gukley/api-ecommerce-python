from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderUpdate
from app.services.order_service import OrderService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User
from app.dependencies.auth import is_moderator
from app.socketio.events import notify_new_order

router = APIRouter()


@router.get(
    "/",
    response_model=list[OrderResponse],
    summary="Obter todos os pedidos do usuário",
    description="Retorna uma lista contendo todos os pedidos feitos pelo usuário autenticado.",
)
def get_orders(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return OrderService.get_orders_by_user(db, current_user)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Obter um pedido específico",
    description="Retorna detalhes de um pedido específico com base no seu ID, desde que pertença ao usuário autenticado.",
    responses={404: {"description": "Pedido não encontrado"}},
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = OrderService.get_order_by_id(db, order_id, current_user)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo pedido",
    description="Cria um novo pedido para o usuário autenticado.",
)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = OrderService.create_order(db, order_data, current_user)

    await notify_new_order(order)

    return order


@router.put(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Atualizar status de um pedido",
    description="Atualiza o status de um pedido específico com base no seu ID. Requer privilégios de moderador.",
    responses={404: {"description": "Pedido não encontrado"}},
)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(is_moderator),
):
    return OrderService.update_order_status(
        db, order_id, order_data.status
    )


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancelar um pedido",
    description="Cancela um pedido específico com base no seu ID, desde que pertença ao usuário autenticado.",
    responses={404: {"description": "Pedido não encontrado"}},
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    OrderService.cancel_order(db, order_id, current_user)
    return


@router.get(
    "/all",
    response_model=list[OrderResponse],
    summary="Obter todos os pedidos",
    description="Retorna uma lista contendo todos os pedidos cadastrados no sistema. Requer privilégios de moderador.",
    responses={401: {"description": "Não autorizado"} , 403: {"description": "Acesso negado"}},
)
def get_all_orders(
    db: Session = Depends(get_db),
    _: User = Depends(is_moderator),
):
    return OrderService.get_all_orders(db)