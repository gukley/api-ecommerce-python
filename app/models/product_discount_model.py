from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ProductDiscount(Base):
    __tablename__ = "product_discounts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    discount_id = Column(
        Integer, ForeignKey("discounts.id", ondelete="CASCADE"), nullable=False
    )

    product = relationship("Product", back_populates="product_discounts")
    discount = relationship("Discount", back_populates="product_discounts")
