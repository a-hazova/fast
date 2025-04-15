from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.schemas import UserRead
from .user_repository import UserRepository
from .user_service import UserService


user_router = APIRouter( 
    prefix='/users',
    tags=['users']
    )

user_service = UserService(repository=UserRepository)

@user_router.get('/{user_id}', description='Get a user by id')
async def get_user(user_id: int, db_session: AsyncSession = Depends(get_session)) -> UserRead:
    return await user_service.get_user(user_id=user_id, session=db_session)
