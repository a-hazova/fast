from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.core.models import Tag
from app.core.schemas import TagCreate

from .tag_repository import  TagRepository

class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository
    
    async def get_tag(self, session: AsyncSession, tag_id: int) -> Tag:
        tag = await self.repository.get_tag(session, tag_id)
        if not tag:
            raise NotFoundError("Tag", "id", tag_id)
        return tag
    
    async def get_tags(self, session: AsyncSession,) -> List[Tag]:
        tags = await self.repository.get_tags(session)
        if not tags:
            raise NotFoundError("Tags")
        return tags
    
    async def create_tag(self, session: AsyncSession, tag: TagCreate) -> Tag:
        tag_in_db = await self.repository.get_tag(session=session, identifier="name", value=tag.name)
        if tag_in_db: 
            raise AlreadyExistsError("Tag", "name", tag.name)
        new_tag = Tag(name = tag.name)
        return await self.repository.create_tag(session, new_tag)
    
    async def delete_tag(self, session: AsyncSession, tag_id: int) -> None:
        tag_in_db = await self.repository.get_tag(session=session, identifier="id", value=tag_id)
        if not tag_in_db:
            raise NotFoundError("Tag", "id", tag_id)
        
        return await self.repository.delete_tag(session, tag_in_db)
