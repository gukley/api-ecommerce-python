from sqlalchemy.orm import Session
from app.repositories.address_repository import AddressRepository
from app.models.address_model import Address
from app.schemas.address_schema import AddressCreate, AddressUpdate
from app.models.user_model import User
from fastapi import HTTPException


class AddressService:
    @staticmethod
    def get_addresses_by_user(db: Session, current_user: User) -> list[Address]:
        return AddressRepository.get_addresses_by_user(db, current_user.id)

    @staticmethod
    def get_address_by_id(db: Session, current_user: User, address_id: int) -> Address:
        return AddressRepository.get_address_by_id(db, address_id, current_user.id)

    @staticmethod
    def create_address(
        db: Session, address_data: AddressCreate, current_user: User
    ) -> Address:
        address = Address(**address_data.model_dump())
        address.user_id = current_user.id
        return AddressRepository.create_address(db, address)

    @staticmethod
    def update_address(
        db: Session, address_id: int, address_data: AddressUpdate, current_user: User
    ) -> Address:
        address = AddressRepository.get_address_by_id(db, address_id)

        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        if address.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not authorized to update this address"
            )

        updates = address_data.model_dump(exclude_unset=True)
        return AddressRepository.update_address(db, address_id, updates)

    @staticmethod
    def delete_address(db: Session, address_id: int, current_user: User):
        address = AddressRepository.get_address_by_id(db, address_id)

        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        if address.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this address"
            )

        AddressRepository.delete_address(db, address_id)
