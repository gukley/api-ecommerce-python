from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from app.repositories.order_repository import OrderRepository
from app.models.order_model import Order, OrderStatus
from app.models.order_item_model import OrderItem
from app.schemas.order_schema import (
    OrderCreate, OrderUpdate, OrderResponse,
    OrderItemResponse, ProductInfo
)
from app.models.user_model import User
from app.services.cart_service import CartService
from app.models.cart_item_model import CartItem
from app.services.coupon_service import CouponService
from app.services.address_service import AddressService
from app.services.product_service import ProductService
from app.schemas.product_schema import ProductBase
from app.utils.email_utils import send_purchase_email  # novo import


class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, user: User) -> Order:
        print("DEBUG: Entrou em create_order")
        print("OrderCreate recebido:", order_data)
        print("Itens recebidos:", getattr(order_data, "items", None))

        if not order_data.items or len(order_data.items) == 0:
            print("DEBUG: Nenhum item recebido no pedido")
            raise HTTPException(status_code=400, detail="Cart is empty")

        try:
            admin_id = ProductService.get_admin_id_by_product_id(db, order_data.items[0].product_id)
            total_amount = order_data.total_amount

            order = OrderService.create_order_entry(db, order_data, user, total_amount, admin_id)
            OrderService.create_order_items_from_payload(db, order, order_data.items)
            CartService.clear_cart(db, user)
            # Popule endereço e itens no objeto order para o e-mail
            order.address = AddressService.get_address_any_user(db, order.address_id)
            order.order_items = OrderRepository.get_order_items_by_order_id(db, order.id)
            # Se tiver método de pagamento, adicione: order.payment_method = ...
            send_purchase_email(user.email, order)  # Enviar e-mail ao usuário
            print("DEBUG: Pedido criado com sucesso")
            return order
        except Exception as e:
            print("ERRO em create_order:", e)
            raise HTTPException(status_code=500, detail=f"Erro interno ao criar pedido: {e}")

    @staticmethod
    def create_order_entry(
        db: Session, order_data: OrderCreate, user: User, total_amount: Decimal, admin_id: int
    ) -> Order:
        address = AddressService.get_address_by_id(db, user, order_data.address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        if order_data.coupon_id:
            coupon = CouponService.get_coupon_by_id(db, order_data.coupon_id)
            total_amount = Decimal(total_amount)
            total_amount = total_amount - (total_amount * coupon.discount_percentage / Decimal(100))

        order = Order(
            user_id=user.id,
            admin_id=admin_id,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            address_id=order_data.address_id,
            coupon_id=order_data.coupon_id,
        )
        try:
            db.add(order)
            db.commit()
            db.refresh(order)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error creating order")
        return order

    @staticmethod
    def create_order_items_from_payload(db: Session, order: Order, items: list):
        order_items = []
        for item in items:
            # Trate possíveis erros de estoque
            try:
                ProductService.decrease_stock(db, item.product_id, item.quantity)
            except Exception as e:
                print(f"Erro ao baixar estoque do produto {item.product_id}: {e}")
                raise HTTPException(status_code=400, detail=f"Erro ao baixar estoque do produto {item.product_id}")
            order_items.append(
                OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
            )
        OrderRepository.create_order_items(db, order_items)

    @staticmethod
    def _build_products_with_quantity(order) -> List[Dict[str, Any]]:
        """
        Build products list including quantity and unit_price so frontend shows correct quantities.
        Each entry mirrors what the frontend expects: { id, product_id, name, image_path, quantity, unit_price, subtotal }
        """
        products: List[Dict[str, Any]] = []
        for item in getattr(order, "order_items", []) or []:
            prod = getattr(item, "product", None)
            product_dict: Dict[str, Any] = {
                "id": getattr(prod, "id", None),
                "product_id": getattr(prod, "id", None),
                "name": getattr(prod, "name", None),
                "image_path": getattr(prod, "image_path", None),
                "image_url": getattr(prod, "image_url", None),
                "quantity": int(item.quantity) if item.quantity is not None else 1,
                "unit_price": float(item.unit_price) if item.unit_price is not None else None,
                "subtotal": float(item.unit_price) * int(item.quantity) if item.unit_price is not None else None
            }
            products.append(product_dict)
        return products

    @staticmethod
    def get_orders_by_user(db: Session, user: User) -> list[OrderResponse]:
        orders = OrderRepository.get_orders_by_user(db, user.id)
        result = []
        for order in orders:
            # Popule products para compatibilidade com frontend antigo, incluindo quantity/unit_price
            products = OrderService._build_products_with_quantity(order)

            # Popule items para o novo padrão
            items = []
            for item in order.order_items:
                items.append(OrderItemResponse(
                    product=ProductInfo(
                        id=item.product.id,
                        name=item.product.name,
                        image_path=getattr(item.product, "image_path", None)
                    ),
                    quantity=item.quantity,
                    unit_price=float(item.unit_price),
                    total_price=float(item.unit_price) * item.quantity
                ))
            order_response = OrderResponse(
                id=order.id,
                order_date=order.order_date,
                address_id=order.address_id,
                coupon_id=order.coupon_id,
                status=order.status,
                items=items,
                user_id=order.user_id,
                total_amount=float(order.total_amount)
            )
            # Adicione products manualmente para compatibilidade (com quantity e unit_price)
            order_response.products = products
            result.append(order_response)
        return result

    @staticmethod
    def get_order_by_id(db: Session, order_id: int, user: User) -> OrderResponse:
        # Note: repository implementation may vary; adjust call if your repository expects different params
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        # Build items
        items = []
        for item in order.order_items:
            items.append(OrderItemResponse(
                product=ProductInfo(
                    id=item.product.id,
                    name=item.product.name,
                    image_path=getattr(item.product, "image_path", None)
                ),
                quantity=item.quantity,
                unit_price=float(item.unit_price),
                total_price=float(item.unit_price) * item.quantity
            ))

        # Build products with quantity so frontend displays correct qty
        products = OrderService._build_products_with_quantity(order)

        # Return response (address handling kept as before in your flow)
        order_response = OrderResponse(
            id=order.id,
            order_date=order.order_date,
            address_id=order.address_id,
            coupon_id=order.coupon_id,
            status=order.status,
            items=items,
            user_id=order.user_id,
            total_amount=float(order.total_amount)
        )
        order_response.products = products
        return order_response

    @staticmethod
    def update_order_status(
        db: Session, order_id: int, status
        ) -> Order:
        """
        status may be an OrderStatus or a string. Normalize/validate here,
        then call repository with an OrderStatus enum.
        """
        if status is None:
            raise HTTPException(status_code=400, detail="Status é obrigatório")

        # Normalize incoming status (accept enum instance or string variants)
        if isinstance(status, OrderStatus):
            status_enum = status
        else:
            s = str(status).strip().upper()
            # common variant mappings
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
                status_enum = OrderStatus(normalized)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Status inválido: {status}. Valores permitidos: {[m.value for m in OrderStatus]}")

        try:
            order = OrderRepository.update_order_status(db, order_id, status_enum)
        except Exception as exc:
            # Log upstream if you have a logger; here we convert to HTTPException
            raise HTTPException(status_code=500, detail="Erro interno ao atualizar status do pedido")
        if not order:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return order

    @staticmethod
    def cancel_order(db: Session, order_id: int, user: User):
        """
        Cancela um pedido específico, garantindo que pertence ao usuário.
        """
        # Busca o pedido garantindo que pertence ao usuário autenticado
        order = OrderRepository.get_order_by_id(db, order_id, user.id)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        # Só permite cancelar se o status for PENDING ou PROCESSING
        if order.status not in (OrderStatus.PENDING, OrderStatus.PROCESSING):
            raise HTTPException(status_code=400, detail="Somente pedidos pendentes ou em processamento podem ser cancelados")

        try:
            order.status = OrderStatus.CANCELLED  # Atualiza o status para CANCELLED
            db.add(order)
            db.commit()
            db.refresh(order)
            return order
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail="Erro interno ao cancelar pedido")

    @staticmethod
    def get_all_orders(db: Session) -> list[OrderResponse]:
        orders = OrderRepository.get_all_orders(db)
        result = []
        for order in orders:
            products = OrderService._build_products_with_quantity(order)
            items = []
            for item in order.order_items:
                items.append(OrderItemResponse(
                    product=ProductInfo(
                        id=item.product.id,
                        name=item.product.name,
                        image_path=getattr(item.product, "image_path", None)
                    ),
                    quantity=item.quantity,
                    unit_price=float(item.unit_price),
                    total_price=float(item.unit_price) * item.quantity
                ))
            order_response = OrderResponse(
                id=order.id,
                order_date=order.order_date,
                address_id=order.address_id,
                coupon_id=order.coupon_id,
                status=order.status,
                items=items,
                user_id=order.user_id,
                total_amount=float(order.total_amount)
            )
            order_response.products = products
            result.append(order_response)
        return result

    @staticmethod
    def get_all_orders_by_admin(db: Session, admin_id: int) -> list[OrderResponse]:
        orders = OrderRepository.get_all_orders_by_admin(db, admin_id)
        result = []
        for order in orders:
            products = OrderService._build_products_with_quantity(order)
            items = []
            for item in order.order_items:
                items.append(OrderItemResponse(
                    product=ProductInfo(
                        id=item.product.id,
                        name=item.product.name,
                        image_path=getattr(item.product, "image_path", None)
                    ),
                    quantity=item.quantity,
                    unit_price=float(item.unit_price),
                    total_price=float(item.unit_price) * item.quantity
                ))
            order_response = OrderResponse(
                id=order.id,
                order_date=order.order_date,
                address_id=order.address_id,
                coupon_id=order.coupon_id,
                status=order.status,
                items=items,
                user_id=order.user_id,
                total_amount=float(order.total_amount)
            )
            order_response.products = products
            result.append(order_response)
        return result

    @staticmethod
    def get_orders_by_user_id(db: Session, user_id: int):
        return db.query(Order).filter(Order.user_id == user_id).all()