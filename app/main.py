import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core import router
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings

MEDIA_DIR = settings.get_media_dir()

app = FastAPI(
    title="Post Service API",
    debug=True
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

app.include_router(router)