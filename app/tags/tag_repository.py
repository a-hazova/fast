from typing import List
from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models import Tag
from app.core.schemas import TagCreate, TagRead


class TagRepository:

    @staticmethod
    async def get_tag(session: AsyncSession, tag_id: int):
        query = select(Tag).where(Tag.id == tag_id)
        result = await session.execute(query)
        if tag:= result.scalar_one_or_none():
            return tag
        raise HTTPException(
            status_code=404, detail=f"Tag with id '{tag_id}' not found")

    @staticmethod
    async def get_tags(session: AsyncSession) -> List[TagRead]:
        query = select(Tag)
        results = await session.execute(query)
        return results.scalars().all()

    @staticmethod
    async def create_tag(session: AsyncSession, tag_in: TagCreate):
        query = select(Tag).where(Tag.name == tag_in.name)
        result = await session.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400, detail=f"Tag '{tag_in.name}' already exists")
        tag_in_db = Tag(name=tag_in.name)
        session.add(tag_in_db)
        await session.commit()
        await session.refresh(tag_in_db)
        return tag_in_db

    @staticmethod
    async def delete_tag(session: AsyncSession, tag_id: int):
        query = select(Tag).where(Tag.id == tag_id)
        result = await session.execute(query)
        if tag := result.scalar_one_or_none():
            await session.delete(tag)
            await session.commit()
        raise HTTPException(
            status_code=404, detail=f"Tag with id '{tag_id}' not found")
