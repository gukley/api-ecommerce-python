from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.address_schema import AddressCreate, AddressResponse, AddressUpdate
from app.services.address_service import AddressService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User

router = APIRouter()


@router.get("/", response_model=list[AddressResponse])
def get_addresses(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return AddressService.get_addresses_by_user(db, current_user)


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AddressService.get_address_by_id(db, current_user, address_id)


@router.post("/", response_model=AddressResponse)
def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AddressService.create_address(db, address_data, current_user)


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AddressService.update_address(db, address_id, address_data, current_user)


@router.delete("/{address_id}", status_code=204)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    AddressService.delete_address(db, address_id, current_user)
    return
