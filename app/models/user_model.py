from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(enum.Enum):
    CLIENT = "CLIENT"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    image_path = Column(String(200), default="/uploads/defaults/no_profile_image.png", nullable=True)

    addresses = relationship("Address", back_populates="user", passive_deletes=True)
    orders = relationship("Order", back_populates="user", passive_deletes=True)
    cart = relationship("Cart", back_populates="user", uselist=False, passive_deletes=True)
