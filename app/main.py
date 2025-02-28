from contextlib import asynccontextmanager
from fastapi import FastAPI
from post_server.core.database import database, setup_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Функция жизненного цикла FastAPI
    логика перед оператором yield — это событие запуска, которое будет запущено один раз перед запуском приложения
    логика после оператора yield — это событие завершения, которое будет запущено один раз после завершения работы приложения
    """
    
    await setup_database()
    yield
    await database.close_database()

app = FastAPI(
    lifespan=lifespan,
    title="Post Service API"
)