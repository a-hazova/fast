from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.exceptions import NotFoundError
from app.users.user_repository import UserRepository
from .auth_schema import AuthLogin, AuthSignUp, TokenData
from .auth_service import AuthService


auth_router = APIRouter( 
    prefix='/auth',
    tags=['authentification']
    )

auth_service = AuthService(repository=UserRepository)

@auth_router.post('/login')
async def log_in(user_cerd: Annotated[AuthLogin, Form()], session: AsyncSession = Depends(get_session)) -> TokenData:
    try:
        return await auth_service.log_in(user_cerd=user_cerd, session=session)
    except NotFoundError as e:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail=str(e))

@auth_router.post('/register', description='Register a new user', status_code=201)
async def sign_up(user_cerd: Annotated[AuthSignUp, Form()], db_session: AsyncSession = Depends(get_session)) -> TokenData:
    return await auth_service.sign_up(user_cerd=user_cerd, session=db_session)