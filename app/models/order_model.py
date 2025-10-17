from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum
import pytz


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


def get_brazil_datetime():
    return datetime.now(pytz.timezone("America/Sao_Paulo"))


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=True)
    order_date = Column(DateTime, nullable=False, default=get_brazil_datetime)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)

    admin_id = Column(Integer, nullable=True)

    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    coupon = relationship("Coupon", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", passive_deletes=True)