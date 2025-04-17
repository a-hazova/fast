from typing import List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models import Tag
from app.utils.get_column import get_column


class TagRepository:

    @staticmethod
    async def get_tag(session: AsyncSession, identifier: str, value: Union[int, str]) -> Tag | None:
        column = get_column(Tag, identifier)
        query = select(Tag).where(column == value)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_bulk_tags(session: AsyncSession, identifier: str, values: list[Union[str, int]]) -> list[Tag]:
        column = get_column(Tag, identifier)
        query = select(Tag).where(column.in_(values))
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_tags(session: AsyncSession) -> List[Tag]:
        query = select(Tag)
        results = await session.execute(query)
        return results.scalars().all()

    @staticmethod
    async def create_tag(session: AsyncSession, tag: Tag):
        session.add(tag)
        await session.commit()
        await session.refresh(tag)
        return tag

    @staticmethod
    async def delete_tag(session: AsyncSession, tag: Tag):
        await session.delete(tag)
        await session.commit()
