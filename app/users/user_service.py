from typing import Union
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_schema import AuthUser
from app.core.exceptions import NotFoundError
from app.core.schemas import UserMe, UserUpdateForm, UserWithPosts
from app.utils.save_image import save_image

from .user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def get_user(self, session: AsyncSession, user_id: int, current_user) -> Union[UserWithPosts, UserMe]:
        user = await self.repository.get_user(session, user_id)
        if not user:
            raise NotFoundError("User", "id", user_id)
        if user_id != current_user.id:
            return UserWithPosts(user)
        return UserMe(user)
    
    async def get_users(self, session: AsyncSession):
        users = await self.repository.get_users(session)
        if not users:
            raise NotFoundError("Users")
    
    async def update_user(self, session: AsyncSession, user_id: int, current_user: AuthUser, update_data: UserUpdateForm) -> UserMe:
        if user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                              detail="Dont have rights to access the source")
        data = update_data.model_dump(exclude_unset=True)
        if data['image']:
            path = save_image(update_data.image.file, current_user.id, update_data.image.filename)
        data['image'] = path

        user = await self.repository.get_user(session=session, identifier='id', value=user_id)
        updated_user = await self.repository.update_user(session, user, data)
        return updated_user
    