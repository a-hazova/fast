from typing import List
from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.model import Post, Tag
from app.schemas.post_schemas import PostRead, PostCreate


class PostRepository:

    @staticmethod
    async def get_post(session: AsyncSession, post_id: int):
        async with session as s:
            query = select(Post).where(Post.id == post_id)
            result = await s.execute(query)
            return result.scalars().first()

    @staticmethod
    async def get_posts(session: AsyncSession) -> List[PostRead]:
        async with session as s:
            query = select(Post)
            results = await s.execute(query)
            all = results.unique().scalars().all()
            return all

    @staticmethod
    async def create_post(session: AsyncSession, post_in: PostCreate):
        tag_query = select(Tag).where(Tag.name.in_(post_in.tags))
        result = await session.execute(tag_query)
        existing_tags = result.scalars().all()
        existing_tags_names = [tag.name for tag in existing_tags]
        for tag_name in post_in.tags:
            if tag_name not in existing_tags_names:
                raise HTTPException(
                    status_code=404, detail=f"Tag '{tag_name}' not found")
        del post_in.tags
        post_in_db = Post(**post_in.model_dump(), tags=existing_tags)

        session.add(post_in_db)
        await session.commit()
        await session.refresh(post_in_db)
        return post_in_db

    @staticmethod
    async def delete_post(session: AsyncSession, post_id: int):
        async with session as s:
            query = delete(Post).where(Post.id == post_id)
            result = await s.execute(query)
            await s.commit()
