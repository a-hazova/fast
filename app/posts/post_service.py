from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_schema import AuthUser
from app.core.schemas import PostCreate, PostInDB, PostRead
from .post_repository import PostRepository


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def get_post(self, session: AsyncSession, post_id: int) -> PostRead:
        return await self.repository.get_post(session, post_id)

    async def get_posts(self, session: AsyncSession,) -> List[PostRead]:
        return await self.repository.get_posts(session)

    async def create_post(self, session: AsyncSession, post_in: PostCreate, current_user: AuthUser) -> PostRead:
        post_in = PostInDB(**post_in.model_dump(), author_id = current_user.id)
        return await self.repository.create_post(session, post_in)

    async def delete_post(self, session: AsyncSession, post_id: int) -> bool:
        return await self.repository.delete_post(session, post_id)
