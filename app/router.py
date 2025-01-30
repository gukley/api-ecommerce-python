from fastapi import APIRouter
from app.controllers.auth_controller import router as auth_router
from app.controllers.user_controller import router as user_router
from app.controllers.address_controller import router as address_router
from app.controllers.category_controller import router as category_router
from app.controllers.discount_controller import router as discount_router
from app.controllers.coupon_controller import router as coupon_router
from app.controllers.product_controller import router as product_router
from app.controllers.cart_controller import router as cart_router
from app.controllers.order_controller import router as order_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(address_router, prefix="/addresses", tags=["Addresses"])
api_router.include_router(category_router, prefix="/categories", tags=["Categories"])
api_router.include_router(discount_router, prefix="/discounts", tags=["Discounts"])
api_router.include_router(coupon_router, prefix="/coupons", tags=["Coupons"])
api_router.include_router(product_router, prefix="/products", tags=["Products"])
api_router.include_router(cart_router, prefix="/cart", tags=["Cart"])
api_router.include_router(order_router, prefix="/orders", tags=["Orders"])
