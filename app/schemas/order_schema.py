from pydantic import BaseModel, field_validator, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.order_model import OrderStatus
from app.schemas.product_schema import ProductBase
from decimal import Decimal
from typing_extensions import Annotated

class AddressSchema(BaseModel):
    id: int
    user_id: Optional[int] = None
    street: Optional[str] = None
    number: Optional[int] = None  # Alterado de str para int
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

class OrderBase(BaseModel):
    address_id: int
    coupon_id: Optional[int] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    payment_method: str
    total_amount: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    shipping_cost: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('status', mode='before')
    def normalize_status(cls, v):
        if v is None:
            return None
        # If already an OrderStatus instance, return it
        if isinstance(v, OrderStatus):
            return v
        s = str(v).strip().upper()
        MAP = {
            'CANCELED': 'CANCELLED',
            'CANCELADO': 'CANCELLED',
            'CANCELLED': 'CANCELLED',
            'PENDENTE': 'PENDING',
            'PENDING': 'PENDING',
            'PROCESSANDO': 'PROCESSING',
            'PROCESSING': 'PROCESSING',
            'ENVIADO': 'SHIPPED',
            'SHIPPED': 'SHIPPED',
            'ENTREGUE': 'COMPLETED',
            'COMPLETED': 'COMPLETED'
        }
        normalized = MAP.get(s, s)
        try:
            return OrderStatus(normalized)
        except ValueError:
            raise ValueError(f"Invalid status: {v}. Valores permitidos: {[m.value for m in OrderStatus]}")

class ProductInfo(BaseModel):
    id: int
    name: str
    image_path: Optional[str] = None  # pode ser None

class OrderItemResponse(BaseModel):
    product: ProductInfo
    quantity: int
    unit_price: float
    total_price: float

class OrderResponse(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    status: OrderStatus
    # Garantir listas por padrão (evita null)
    items: List[OrderItemResponse] = []
    user_id: int
    total_amount: float

    # Campo adicionado para compatibilidade com frontend antigo:
    # aceitar lista de dicionários (possuindo keys: id, name, image_path, quantity, unit_price, etc.)
    products: List[Dict[str, Any]] = []

    # Incluir endereço completo (opcional) para que o frontend não precise
    # fazer chamada separada a /addresses/{id}
    address: Optional[AddressSchema] = None

    model_config = ConfigDict(from_attributes=True)