from fastapi import FastAPI, Depends
from app.router import api_router

app = FastAPI(debug=True)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
