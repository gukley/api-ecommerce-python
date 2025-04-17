from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.tag_repository import TagRepository
from app.models.tag_model import Tag
from app.schemas.tag_schema import TagCreate, TagUpdate
from app.repositories.product_repository import ProductRepository
from app.models.product_model import Product

class TagService:
    @staticmethod
    def get_all_tags(db: Session) -> list[Tag]:
        return TagRepository.get_all_tags(db)

    @staticmethod
    def get_tag_by_id(db: Session, tag_id: int) -> Tag:
        return TagRepository.get_tag_by_id(db, tag_id)

    @staticmethod
    def create_tag(db: Session, tag_data: TagCreate) -> Tag:
        tag = tag(**tag_data.model_dump())

        if TagRepository.get_tag_by_code(db, tag.code):
            raise HTTPException(status_code=400, detail="Tag code already exists")

        return TagRepository.create_tag(db, tag)

    @staticmethod
    def update_tag(db: Session, tag_id: int, tag_data: TagUpdate) -> Tag:
        updates = tag_data.model_dump(exclude_unset=True)
        tag = TagRepository.get_tag_by_id(db, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        tag = TagRepository.get_tag_by_code(db, tag_data.code)
        if tag:
            raise HTTPException(status_code=400, detail="Tag code already exists")

        return TagRepository.update_tag(db, tag_id, updates)

    @staticmethod
    def delete_tag(db: Session, tag_id: int):
        TagRepository.delete_tag(db, tag_id)

    @staticmethod
    def add_product_to_tag(db: Session, tag_id: int, product_id: int) -> list[Product]:
        tag = TagRepository.get_tag_by_id(db, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        product = ProductRepository.get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product in tag.products:
            raise HTTPException(status_code=400, detail="Product already in tag")

        tag.products.append(product)
        db.commit()
        db.refresh(tag)
        return tag.products

    @staticmethod
    def remove_product_from_tag(db: Session, tag_id: int, product_id: int) -> list[Product]:
        tag = TagRepository.get_tag_by_id(db, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        product = ProductRepository.get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product not in tag.products:
            raise HTTPException(status_code=400, detail="Product not in tag")

        tag.products.remove(product)
        db.commit()
        db.refresh(tag)        
        return tag.products