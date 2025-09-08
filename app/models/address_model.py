from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    street = Column(String(200), nullable=False)
    number = Column(Integer, nullable=False)
    zip = Column(String(8), nullable=False)  # Ajuste para 8 caracteres
    bairro = Column(String(100), nullable=False)  # Novo campo bairro
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")

