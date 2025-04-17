from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), nullable=False, unique=True)
    color_hex = Column(String(7), nullable=False, default="#000000")
    description = Column(String(500), nullable=True)

    product_links = relationship("TagProduct", back_populates="tag")

    products = relationship("Product", secondary="tag_products", viewonly=True)