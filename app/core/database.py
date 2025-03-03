from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Optional, Type, TypeVar
from sqlalchemy import text, select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import env_vars
from app.logger import logger
from app.schemas.base import Base, BaseInDB

ModelType = TypeVar('ModelType', bound=Base)
InDBSchemaType = TypeVar('InDBSchemaType', bound=BaseInDB)


# Создание модуля подключения к базе данных
class Database:
    def __init__(self):

        # Использование асинхронного движка предотвращает блокировку цикла событий запросами к базе данных,
        # позволяя FastAPI обрабатывать несколько запросов одновременно. Это особенно полезно в ситуациях с большим трафиком,
        # например, в приложениях для чата в реальном времени,
        # где множество пользователей одновременно обращаются к базе данных.

        # echo=True позволяет выводит SQL-запросы в консоли, должно иметь значение False в проде.
        # future=True совместимость с кодстилем SQLAlchemy 2.0.
        self.engine = create_async_engine(
            "postgresql+asyncpg://postgres:postgres@localhost:5432/postdb", echo=True, future=True)

        # используется для создания базового класса моделей.
        self.Base = declarative_base()

    async def create_database(self, database_name: str):
        """
        Этот метод подключается к базе данных PostgreSQL (обычно postgres) и проверяет, существует целевая база данных (например, database_name = «bookdb»)
        Пользователь базы данных должен быть суперпользователем или иметь права администратора (например, postgres), который может выполнять запросы CREATE DATABASE.
        """

        # isolation_level="AUTOCOMMIT": этот параметр гарантирует, что команда CREATE DATABASE не будет заключена в транзакцию.
        superuser_db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/postdb"
        superuser_engine = create_async_engine(
            superuser_db_url, echo=True, future=True, isolation_level="AUTOCOMMIT")

        try:
            async with superuser_engine.connect() as conn:
                result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'"))
                db_exists = result.scalar()
                if not db_exists:
                    await conn.execute(text(f"CREATE DATABASE '{database_name}'"))
                    logger.info('База данных создана')
                else:
                    logger.info('База данных уже существует')
        except ProgrammingError as e:
            logger.error(f'Ошибка при создании базы данных')
        finally:
            await superuser_engine.dispose()

    async def ping_database(self):
        """
        Хорошей практикой является проверка соединения с базой данных перед выполнением любых операций. 
        Это предотвращает выполнение запросов приложением, когда база данных недоступна, избегая ошибок или потери данных.
        """

        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Подключение к базе данных прошло успешно")
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")

    async def create_tables(self):
        """
        Создание таблицы из моделей SQLAlchemy. 
        Сопоставляет модели Python с таблицами SQL, гарантируя, что таблицы готовы к хранению данных.
        """

        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)
        logger.info("Таблицы базы данных успешно созданы")

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        """
        @asynccontextmanager используется для управления асинхронными ресурсами (например, соединениями с базой данных, сетевыми сокетами), 
        которым требуется та же настройка и функциональность удаления.

        sessionmaker используется для создания сеансов, которые служат интерфейсом к нашей базе данных. 
        С sessionmaker каждый запрос получает свой собственный сеанс, гарантируя, что операции базы данных изолированы друг от друга.

        async with гарантирует, что сеансы используются безопасно, позволяя выполнять автоматическую очистку при выходе из контекста.
        session.rollback() вызывается в случае возникновения ошибки, гарантируя, что любые частичные изменения будут отменены для поддержания согласованности данных.
        session.close() гарантирует, что сеанс закрывается после каждой транзакции, освобождая ресурсы для других операций.
        """

        async_session = sessionmaker(self.engine, class_=AsyncSession)
        session = None
        try: 
            session = async_session()
            async with session:
                yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
            
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, Any]:
        Session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        async with Session() as session:
            yield session

    async def close_database(self):
        """
        Метод для корректного закрытия ядра базы данных при остановке приложения
        """

        await self.engine.dispose()
        logger.info("Подключение к базе данных закрыто")

    async def get(self,
                  session: AsyncSession,
                  *,
                  table_model: Type[ModelType],
                  query_filter=None,
                  ) -> list[ModelType]:
        """
        Метод для получения записей из базы данных

        :param session: Сессия базы данных
        :param table_model: Модель таблицы SQLAlchemy
        :param query_filter: ��ильтр для выборки записей
        :return: Mодель записей
        """

        query = select(table_model)
        if query_filter:
            query = query.filter(query_filter)
        result = await session.execute(query)
        return result.scalars().first()

    async def bulk_get(self,
                       session: AsyncSession,
                       *,
                       table_model: Type[ModelType],
                       query_filter=None,
                       limit: Optional[int] = None,
                       ) -> list[ModelType]:
        """
        Метод для получения записей из базы данных

        :param session: Сессия базы данных
        :param table_model: Модель таблицы SQLAlchemy
        :param query_filter: ��ильтр для выборки записей
        :param limit: Количество записей для выборки
        :return: Список моделей записей
        """

        query = select(table_model)
        if query_filter:
            query = query.filter(query_filter)
        if limit:
            query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def create(self, 
                     session: AsyncSession, 
                     *,
                     obj_to_create: InDBSchemaType,
                     ) -> ModelType:
        """
        Метод для создания записи в базе данных

        :param session: Сессия базы данных
        :param object_to_create: Модель объекта для создания

        :return: Созданная запись
        """
        async with session as s:
            db_object = obj_to_create.to_orm()
            s.add(db_object)
            await s.commit()
            await s.refresh(db_object)
            return db_object
        
        # db_object = obj_to_create.to_orm()
        # session.add(db_object)
        # await session.commit()
        # await session.refresh(db_object)
        # return db_object


database = Database()


async def setup_database():
    await database.create_database("postdb")
    await database.ping_database()
    await database.create_tables()
