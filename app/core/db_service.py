from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Database
from app.models.model import Tag
from app.schemas.tag_schemas import TagInDB

class DBService:
    def __init__(self):
        self._database = Database()
    
    async def create_tag(self, session: AsyncSession, *, tag_in: TagInDB ) -> Tag:
        
        return await self._database.create(session, obj_to_create=tag_in)

db_service = DBService()