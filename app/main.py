from fastapi import FastAPI
from app.routers import router

app = FastAPI(
    title="Post Service API"
)

app.include_router(router)