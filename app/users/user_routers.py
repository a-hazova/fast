from typing import Annotated, List
from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import oauth2
from app.auth.auth_schema import AuthUser
from app.core.database import get_session
from app.core.schemas import UserMe, UserUpdateForm, UserWithPosts
from .user_repository import UserRepository
from .user_service import UserService


user_router = APIRouter( 
    prefix='/users',
    tags=['users']
    )

user_service = UserService(repository=UserRepository)

@user_router.get('', description='Get a users info')
async def get_users( db_session: AsyncSession = Depends(get_session)) -> List[UserWithPosts]:
    return await user_service.get_users(session=db_session)

@user_router.get('/{user_id}', description='Get a user by id')
async def get_user(user_id: int, db_session: AsyncSession = Depends(get_session)) -> UserWithPosts:
    return await user_service.get_user(user_id=user_id, session=db_session)

@user_router.patch('/{user_id}', description='Update_profile')
async def update_user(user_id: int, user_in: Annotated[UserUpdateForm, Form(media_type="multipart/form-data")], db_session: AsyncSession = Depends(get_session), current_user: AuthUser = Depends(oauth2.get_current_user)) -> UserMe:
    return await user_service.update_user(user_id=user_id, current_user=current_user, session=db_session, update_data=user_in)
