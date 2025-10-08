from fastapi import FastAPI
from app.api_router import api_router
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.socketio import socketio_app
import app.socketio.events

app = FastAPI(debug=True)

# CORS liberado para desenvolvimento (todos os domínios)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  
    allow_credentials=True,
    allow_methods=["*"],   # permitir todos os métodos (GET, POST, PUT, DELETE...)
    allow_headers=["*"],   # permitir todos os headers
)

# Rotas da API
app.include_router(api_router)

# Arquivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/socket", socketio_app)

# Custom OpenAPI com Bearer Auth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Generic Marketplace API",
        version="1.0.0",
        description="API for Generic Marketplace developed with FastAPI for CodeAcademy",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
