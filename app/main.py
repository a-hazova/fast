from fastapi import FastAPI
from app.core import router
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(router)