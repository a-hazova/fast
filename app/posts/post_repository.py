from typing import List
from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.models import Post
from app.core.schemas import PostCreate, PostWithAuthor
from app.core.models import Tag


class PostRepository:

    @staticmethod
    async def get_post(session: AsyncSession, post_id: int):
        query = select(Post).options(selectinload(Post.author)).where(Post.id == post_id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_posts(session: AsyncSession) -> List[PostWithAuthor]:
        query = select(Post).options(selectinload(Post.author))
        results = await session.execute(query)
        all = results.unique().scalars().all()
        return all

    @staticmethod
    async def create_post(session: AsyncSession, post_in: PostCreate, user_id: int):
        tags = post_in['tags']
        tag_query = select(Tag).where(Tag.name.in_(tags))
        result = await session.execute(tag_query)
        existing_tags = result.scalars().all()
        existing_tags_names = [tag.name for tag in existing_tags]
        for tag_name in tags:
            if tag_name not in existing_tags_names:
                raise HTTPException(
                    status_code=404, detail=f"Tag '{tag_name}' not found")
            
        post_in['tags'] = existing_tags
        post_in_db = Post(**post_in, author_id=user_id)
        session.add(post_in_db)
        await session.commit()
        await session.refresh(post_in_db)
        return post_in_db

    @staticmethod
    async def delete_post(session: AsyncSession, post_id: int):
        query = delete(Post).where(Post.id == post_id)
        result = await session.execute(query)
        await session.commit()
