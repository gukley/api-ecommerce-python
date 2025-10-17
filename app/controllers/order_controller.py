from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderUpdate
from app.services.order_service import OrderService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User
from app.dependencies.auth import is_moderator
from app.socketio.events import notify_new_order
from app.models.order_model import Order
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

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
    try:
        OrderService.cancel_order(db, order_id, current_user)
        return
    except HTTPException:
        # Re-lança erros HTTP intencionais (404, 403, 400)
        raise
    except Exception as exc:
        logger.exception("Erro ao cancelar pedido %s para usuário %s: %s", order_id, getattr(current_user, "id", None), exc)
        raise HTTPException(status_code=500, detail="Erro interno ao cancelar pedido")


@router.get(
    "/all/{admin_id}",
    response_model=list[OrderResponse],
    summary="Obter todos os pedidos de uma loja especifica",
    description="Retorna uma lista contendo todos os pedidos cadastrados no sistema. Requer privilégios de moderador.",
    responses={401: {"description": "Não autorizado"} , 403: {"description": "Acesso negado"}},
)
def get_orders_by_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Se o usuário for moderador, use admin_id para filtrar pedidos do admin principal
    if current_user.admin_id and current_user.admin_id == admin_id:
        admin_id = current_user.admin_id

    return OrderService.get_all_orders_by_admin(db, admin_id)

@router.get(
    "/user/{user_id}",
    summary="Obter pedidos de um cliente específico",
    response_model=list[dict],  # Ou crie um schema específico se quiser tipar melhor
    description="Retorna todos os pedidos de um cliente, incluindo produtos.",
)
def get_orders_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = OrderService.get_orders_by_user_id(db, user_id)
    result = []
    for order in orders:
        products = []
        for item in order.order_items:
            products.append({
                "id": item.product.id,
                "name": item.product.name,
                "quantity": item.quantity,
                "price": float(item.unit_price),
                "unit_price": float(item.unit_price)
            })
        result.append({
            "id": order.id,
            "status": order.status.value if hasattr(order.status, "value") else str(order.status),
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "total": float(order.total_amount),
            "products": products
        })
    return result

@router.get(
    "/orders/",
    summary="Listar pedidos do usuário autenticado",
    description="Retorna todos os pedidos do usuário atualmente autenticado.",
    responses={
        401: {"description": "Não autorizado"},
        404: {"description": "Nenhum pedido encontrado"},
    },
)
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Busca os pedidos do usuário autenticado
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="Nenhum pedido encontrado")

    # Retorna os pedidos
    return [
        {
            "id": order.id,
            "total_amount": order.total_amount,
            "status": order.status.value if hasattr(order.status, "value") else order.status,
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                }
                for item in order.order_items
            ],
        }
        for order in orders
    ]