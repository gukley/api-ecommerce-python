from sqlalchemy.orm import Session
from app.models.tag_model import Tag
from sqlalchemy.orm import joinedload


class TagRepository:
    @staticmethod
    def get_tag_by_id(db: Session, tag_id: int) -> Tag:
        return (
            db.query(Tag)
            .options(joinedload(Tag.products))
            .filter(Tag.id == tag_id)
            .first()
        )

    @staticmethod
    def get_all_tags(db: Session) -> list[Tag]:
        return db.query(Tag).options(joinedload(Tag.products)).all()

    @staticmethod
    def get_tag_by_code(db: Session, tag_code: str) -> Tag:
        return db.query(Tag).filter(Tag.code == tag_code).first()

    @staticmethod
    def create_tag(db: Session, tag: Tag) -> Tag:
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def update_tag(db: Session, tag_id: int, updates: dict) -> Tag:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            for key, value in updates.items():
                setattr(tag, key, value)
            db.commit()
            db.refresh(tag)
        return tag

    @staticmethod
    def delete_tag(db: Session, tag_id: int):
        tag = db.query(tag).filter(Tag.id == tag_id).first()
        if tag:
            db.delete(tag)
            db.commit()
