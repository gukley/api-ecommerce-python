from fastapi import Form, File, UploadFile
from typing import Optional, Union
from app.schemas.product_schema import ProductCreate
from app.services.image_service import ImageService

async def product_create_form(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    category_id: int = Form(...),
    image: Optional[Union[UploadFile, str]] = File(None),
) -> ProductCreate:
    return ProductCreate(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id,
        image_path=ImageService.save_image(image, "products")
    )
