# app/main.py

from fastapi import FastAPI
from .api.v1.routes import api_router

app = FastAPI()

app.include_router(api_router, prefix="/v1")
