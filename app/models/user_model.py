from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date
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
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Novos campos
    cpf = Column(String(11), nullable=True, index=True)        # armazenar apenas dígitos
    phone = Column(String(20), nullable=True)                  # formato E.164 (ex: +5511999998888)
    birthdate = Column(Date, nullable=True)

    addresses = relationship("Address", back_populates="user", passive_deletes=True)
    orders = relationship("Order", back_populates="user", passive_deletes=True)
    cart = relationship("Cart", back_populates="user", uselist=False, passive_deletes=True)
    favorites = relationship("Favorite", back_populates="user", passive_deletes=True)
    reviews = relationship("Review", back_populates="user", passive_deletes=True)
    admin = relationship("User", remote_side="User.id", backref="moderators")