from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.address_schema import AddressCreate, AddressResponse, AddressUpdate
from app.services.address_service import AddressService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User

router = APIRouter()


@router.get(
    "/",
    response_model=list[AddressResponse],
    summary="Obter todos os endereços do usuário",
    description="Retorna todos os endereços cadastrados pelo usuário autenticado.",
)
def get_addresses(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return AddressService.get_addresses_by_user(db, current_user)


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Obter um endereço específico",
    description="Retorna detalhes de um endereço específico com base no seu ID, desde que pertença ao usuário autenticado.",
    responses={404: {"description": "Endereço não encontrado"}},
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Certifique-se de que o address_id pertence ao usuário autenticado
    address = AddressService.get_address_by_id(db, current_user, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return address


@router.post(
    "/",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo endereço",
    description="Cria um novo endereço associado ao usuário autenticado.",
)
def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AddressService.create_address(db, address_data, current_user)


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Atualizar um endereço",
    description="Atualiza um endereço específico do usuário autenticado com base no seu ID.",
    responses={404: {"description": "Endereço não encontrado"}},
)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AddressService.update_address(db, address_id, address_data, current_user)


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir um endereço",
    description="Exclui um endereço específico do usuário autenticado com base no seu ID.",
    responses={404: {"description": "Endereço não encontrado"},  401: {"description": "Não autorizado"},},
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verifique se o endereço está vinculado a algum pedido
    from app.models.order_model import Order
    if db.query(Order).filter(Order.address_id == address_id).first():
        raise HTTPException(status_code=400, detail="Este endereço está vinculado a pedidos e não pode ser excluído.")
    AddressService.delete_address(db, address_id, current_user)
    return

# Nenhuma alteração necessária aqui, pois os schemas já incluem bairro e zip

