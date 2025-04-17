from collections.abc import AsyncGenerator
from sqlalchemy import exc
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine, async_sessionmaker
import valkey.asyncio as valkey

from app.logger import logger
from app.settings import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except exc.SQLAlchemyError as error:
            await session.rollback()
            logger.error(error)
            raise
        finally:
            await session.close()


valkey_client = valkey.Valkey(host='localhost', port=6379, db=0)

async def get_valkey():
    return valkey_client
