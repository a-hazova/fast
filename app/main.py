from fastapi import FastAPI
from app.core import router

app = FastAPI(
    title="Post Service API"
)

app.include_router(router)