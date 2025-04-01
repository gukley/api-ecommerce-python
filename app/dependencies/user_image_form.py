from fastapi import Form, File, UploadFile
from typing import Optional, Union
from app.schemas.user_schema import UserImageUpdate
from app.services.image_service import ImageService

async def user_image_form(
    image: Optional[Union[UploadFile, str]] = File(None),
) -> UserImageUpdate:
    return UserImageUpdate(
        image_path=ImageService.save_image(image, "profile")
    )
