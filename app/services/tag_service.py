from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tag_schemas import TagRead, TagCreate
from app.repositories.tag_repository import TagRepository


class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository
    
    async def get_tag(self, session: AsyncSession, tag_id: int) -> TagRead:
        return await self.repository.get_tag(session, tag_id)
    
    async def get_tags(self, session: AsyncSession,) -> List[TagRead]:
        return await self.repository.get_tags(session)
    
    async def create_tag(self, session: AsyncSession, tag_in: TagCreate) -> TagRead:
        return await self.repository.create_tag(session, tag_in)
    
    async def delete_tag(self, session: AsyncSession, tag_id: int) -> bool:
        return await self.repository.delete_tag(session, tag_id)
