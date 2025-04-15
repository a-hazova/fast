from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.auth_schema import AuthLogin, AuthSignUp
from app.core.models import User
from app.core.schemas import UserRead



class UserRepository:
    @staticmethod
    async def get_user(session: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_user(session: AsyncSession, user_in: AuthSignUp) -> UserRead:
        user = User(**user_in.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    @staticmethod
    async def get_user_by_username(user_cerd: AuthLogin, session: AsyncSession):
        query = select(User).where(User.username == user_cerd.username)
        result = await session.execute(query)
        return result.scalars().first()
    