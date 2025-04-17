from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class TagProduct(Base):
    __tablename__ = "tag_products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

    product = relationship("Product", back_populates="tag_links")
    tag = relationship("Tag", back_populates="product_links")
