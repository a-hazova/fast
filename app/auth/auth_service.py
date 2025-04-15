from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_repository import UserRepository
from app.utils import hash_password, verify_password
from .auth_schema import AuthLogin, TokenData, AuthSignUp
from .oauth2 import create_access_token


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def login_user(self, session: AsyncSession, user_cerd: AuthLogin) -> TokenData:
        user = await self.repository.get_user_by_username(session=session, user_cerd=user_cerd)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User with provided email not found"
            )
        if not verify_password(user_cerd.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials'
            )
        token = create_access_token(data = {'user_id': user.id})
        return TokenData(access_token=token, token_type='bearer')
    
    async def create_user(self, session: AsyncSession, user_cerd: AuthSignUp) -> TokenData:
        hashed_password = hash_password(user_cerd.password)
        user_cerd.password = hashed_password
        user =  await self.repository.create_user(user_in=user_cerd, session=session)
        token = create_access_token(data = {'user_id': user.id})
        return TokenData(access_token=token, token_type='bearer')
        

   
