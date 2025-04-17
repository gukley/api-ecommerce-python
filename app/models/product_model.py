from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(200), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    image_path = Column(String(200), nullable=True)
    description = Column(String(500), nullable=True)

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product", passive_deletes=True)
    order_items = relationship("OrderItem", back_populates="product", passive_deletes=True)
    discounts = relationship("Discount", back_populates="product", passive_deletes=True)
    tags = relationship("Tag", secondary="product_tags", viewonly=True)
    tag_links = relationship("ProductTag", back_populates="product")