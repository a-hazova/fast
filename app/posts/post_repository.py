from typing import List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.models import Post
from app.core.schemas import PostWithAuthor
from app.core.models import Tag
from app.utils.get_column import get_column


class PostRepository:

    @staticmethod
    async def get_post(session: AsyncSession, identifier: str, value: Union[int, str]):
        column = get_column(Post, identifier)
        query = select(Post).options(selectinload(Post.author)).where(column == value)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_posts(session: AsyncSession) -> List[PostWithAuthor]:
        query = select(Post).options(selectinload(Post.author))
        results = await session.execute(query)
        return results.unique().scalars().all()

    @staticmethod
    async def create_post(session: AsyncSession, post: dict, user_id: int, tags: list[Tag]) -> Post:
        post_in_db = Post(**post, author_id=user_id, tags=tags)
        session.add(post_in_db)
        await session.commit()
        await session.refresh(post_in_db)
        return post_in_db

    @staticmethod
    async def delete_post(session: AsyncSession, post: Post):
        await session.delete(post)
        await session.commit()
