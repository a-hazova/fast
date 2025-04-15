from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import UserRead

from .user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def get_user(self, session: AsyncSession, user_id: int) -> UserRead:
        return await self.repository.get_user(session, user_id)
    