from sqlalchemy.orm import Session
from app.models.address_model import Address


class AddressRepository:
    @staticmethod
    def get_addresses_by_user(db: Session, user_id: int) -> list[Address]:
        return db.query(Address).filter(Address.user_id == user_id).all()

    @staticmethod
    def get_address_by_id(db: Session, address_id: int, user_id: int) -> Address:
        return (
            db.query(Address)
            .filter(Address.id == address_id, Address.user_id == user_id)
            .first()
        )

    @staticmethod
    def create_address(db: Session, address: Address) -> Address:
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def update_address(db: Session, address_id: int, updates: dict) -> Address:
        db.query(Address).filter(Address.id == address_id).update(updates)
        db.commit()
        return db.query(Address).filter(Address.id == address_id).first()

    @staticmethod
    def delete_address(db: Session, address_id: int):
        db.query(Address).filter(Address.id == address_id).delete()
        db.commit()

    @staticmethod
    def get_address_by_id_any(db: Session, address_id: int) -> Address:
        return db.query(Address).filter(Address.id == address_id).first()