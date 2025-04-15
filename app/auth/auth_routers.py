from typing import Annotated
from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.users.user_repository import UserRepository
from .auth_schema import AuthLogin, AuthSignUp, TokenData
from .auth_service import AuthService


auth_router = APIRouter( 
    prefix='/auth',
    tags=['authentification']
    )

auth_service = AuthService(repository=UserRepository)

@auth_router.post('/login')
async def login(user_cerd: Annotated[AuthLogin, Form()], session: AsyncSession = Depends(get_session)) -> TokenData:
    token = await auth_service.login_user(user_cerd=user_cerd, session=session)
    return token

@auth_router.post('/register', description='Register a new user', status_code=201)
async def create_user(user_cerd: Annotated[AuthSignUp, Form()], db_session: AsyncSession = Depends(get_session)) -> TokenData:
    return await auth_service.create_user(user_cerd=user_cerd, session=db_session)