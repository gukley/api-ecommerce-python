from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.coupon_schema import CouponCreate, CouponResponse, CouponUpdate
from app.services.coupon_service import CouponService
from app.dependencies.auth import is_admin

router = APIRouter()


@router.get(
    "/",
    response_model=list[CouponResponse],
    summary="Obter todos os cupons",
    description="Retorna uma lista contendo todos os cupons disponíveis no sistema.",
)
def get_coupons(db: Session = Depends(get_db)):
    return CouponService.get_all_coupons(db)


@router.get(
    "/{coupon_id}",
    response_model=CouponResponse,
    summary="Obter um cupom específico",
    description="Retorna detalhes de um cupom específico com base no seu ID.",
    responses={404: {"description": "Cupom não encontrado"}},
)
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    coupon = CouponService.get_coupon_by_id(db, coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return coupon


@router.post(
    "/",
    response_model=CouponResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo cupom",
    description="Cria um novo cupom. Requer privilégios de administrador.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def create_coupon(
    coupon_data: CouponCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    return CouponService.create_coupon(db, coupon_data)


@router.put(
    "/{coupon_id}",
    response_model=CouponResponse,
    summary="Atualizar um cupom",
    description="Atualiza informações de um cupom específico com base no seu ID. Requer privilégios de administrador.",
    responses={
        404: {"description": "Cupom não encontrado"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def update_coupon(
    coupon_id: int,
    coupon_data: CouponUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    return CouponService.update_coupon(db, coupon_id, coupon_data)


@router.delete(
    "/{coupon_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir um cupom",
    description="Exclui um cupom específico com base no seu ID. Requer privilégios de administrador.",
    responses={
        404: {"description": "Cupom não encontrado"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    CouponService.delete_coupon(db, coupon_id)
