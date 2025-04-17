from typing import List, Union
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.models import User
from app.core.schemas import UserMe, UserWithPosts
from app.utils.get_column import get_column


class UserRepository:
    @staticmethod
    async def get_user(session: AsyncSession, identifier: str, value: Union[int, str]) -> User:
        column = get_column(User, identifier)
        query = select(User).where(column == value)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_users(session: AsyncSession) -> List[UserWithPosts]:
        query = select(User).options(selectinload(User.posts))
        result = await session.execute(query)
        return result.unique().scalars().all()
        
    @staticmethod
    async def create_user(session: AsyncSession, user_in: dict) -> UserWithPosts:
        user = User(**user_in)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    @staticmethod
    async def update_user(session: AsyncSession, user: User, update_data: dict) -> UserMe:
        query = update(User).where(User.id == user.id).values(**update_data).returning(User)
        result = await session.execute(query)
        await session.commit()  
        await session.refresh(user) 
        return result.scalar_one_or_none()
    