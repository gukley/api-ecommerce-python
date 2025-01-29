from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(200), nullable=False)
    discount_percentage = Column(DECIMAL(5, 2), nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)

    product_discounts = relationship("ProductDiscount", back_populates="discount")
