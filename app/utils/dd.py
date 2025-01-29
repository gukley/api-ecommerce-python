from fastapi.responses import JSONResponse
from pydantic import BaseModel


def dd(data):
    if isinstance(data, BaseModel):
        data = data.dict()
    return JSONResponse(content=data, status_code=200)
