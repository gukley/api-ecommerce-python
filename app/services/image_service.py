import shutil
import os
from fastapi import UploadFile, HTTPException   
from typing import Optional
from uuid import uuid4

class ImageService:
    @staticmethod
    def save_image(image: Optional[UploadFile], source: str) -> str:
        UPLOAD_DIR = "uploads/" + source
        DEFAULT_IMAGE = "uploads/defaults/no_product_image.png"
        ALLOWED_TYPES = ["image/jpeg", "image/png"]

        if image and image.__class__.__name__ == "UploadFile" and image.filename:
            if image.content_type not in ALLOWED_TYPES:
                raise HTTPException(status_code=400, detail="Apenas arquivos JPG ou PNG são permitidos.")

            extension = image.filename.split(".")[-1]
            filename = f"{uuid4()}.{extension}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            os.makedirs(UPLOAD_DIR, exist_ok=True)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            image_path = f"/{file_path}"
        else:
            image_path = f"/{DEFAULT_IMAGE}"

        return image_path