from typing import List
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.auth.auth_schema import AuthLogin, AuthSignUp
from app.core.models import User
from app.core.schemas import UserMe, UserWithPosts



class UserRepository:
    @staticmethod
    async def get_user(session: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_users(session: AsyncSession) -> List[UserWithPosts]:
        query = select(User).options(selectinload(User.posts))
        result = await session.execute(query)
        all_users = result.unique().scalars().all()
        print(all_users)
        return all_users

    @staticmethod
    async def create_user(session: AsyncSession, user_in: AuthSignUp) -> UserWithPosts:
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

    @staticmethod
    async def update_user(session: AsyncSession, user_id, user_update) -> UserMe:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for field, value in user_update.items():
            setattr(user, field, value)

        await session.commit()
        await session.refresh(user) 
        return user
    