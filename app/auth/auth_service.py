from datetime import datetime, timezone
from typing import Tuple
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CredentialsError, NotFoundError
from app.core.schemas import UserUpdateForm
from app.users.user_repository import UserRepository
from app.utils import hash_password, verify_password
from .auth_schema import AuthLogin, AuthUser,TokenData, AuthSignUp
from .oauth2 import blacklist_token, create_access_token, create_refresh_token, verify_refresh_token, verify_token

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def log_in(self, session: AsyncSession, user_cerd: AuthLogin) -> Tuple[str, TokenData]:
        user = await self.repository.get_user(session=session, identifier="username", value=user_cerd.username)
        if not user:
            raise NotFoundError("User", "username", user_cerd.username)
        if not verify_password(user_cerd.password, user.password):
            raise NotFoundError(error_message='Invalid Credentials')
        
        access_token = create_access_token(data = {'sub': str(user.id)})
        refresh_token = create_refresh_token(data = {'sub': str(user.id)})
        
        return (refresh_token, TokenData(access_token=access_token, token_type='bearer'))
    
    async def sign_up(self, session: AsyncSession, user_cerd: AuthSignUp) -> Tuple[str, TokenData]:
        hashed_password = hash_password(user_cerd.password)
        user_cerd.password = hashed_password
        user =  await self.repository.create_user(user_in=user_cerd, session=session)

        access_token = create_access_token(data = {'sub': str(user.id)})
        refresh_token = create_refresh_token(data = {'sub': str(user.id)})

        return (refresh_token, TokenData(access_token=access_token, token_type='bearer'))
        
    
    async def get_refresh_token(self, token: str, session: AsyncSession) -> Tuple[str, TokenData]:
        token_data = await verify_refresh_token(token, session)
        if not token_data['sub']:
            raise CredentialsError()
    
        user =  await self.repository.get_user(identifier="id", value=int(token_data['sub']), session=session)
        if not user:
            raise NotFoundError(error_message="User not found")
        
        access_token = create_access_token(data = {'sub': str(user.id)})
        refresh_token = create_refresh_token(data = {'sub': str(user.id)}) 

        return (refresh_token, TokenData(access_token=access_token, token_type='bearer'))
    
   
    async def sign_out_from_all_devices(self, current_user, session: AsyncSession):
        ts = int(datetime.now(timezone.utc).timestamp())
        update_data = UserUpdateForm(invalidate_before=ts).model_dump(exclude_none=True)
        updated_user = await self.repository.update_user(session, current_user, update_data)
        
        if not updated_user:
            raise NotFoundError(error_message="User with given credentials is not found")
        