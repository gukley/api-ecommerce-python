from fastapi import Form, File, UploadFile
from typing import Optional, Union
from app.schemas.category_schema import CategoryCreate
from app.services.image_service import ImageService

async def category_create_form(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    image: Optional[Union[UploadFile, str]] = File(None),
) -> CategoryCreate:
    return CategoryCreate(
        name=name,
        description=description,
        image_path=ImageService.save_image(image, "categories")
    )
