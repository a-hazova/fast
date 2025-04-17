from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import oauth2
from app.auth.oauth2 import blacklist_token
from app.core.database import get_session, get_valkey
from app.core.exceptions import CredentialsError, NotFoundError
from app.users.user_repository import UserRepository
from .auth_schema import AuthLogin, AuthSignUp, AuthUser, TokenData
from .auth_service import AuthService


auth_router = APIRouter(
    prefix='/auth',
    tags=['authentification']
)

auth_service = AuthService(repository=UserRepository)


@auth_router.post('/login', description='Get access token', status_code=status.HTTP_200_OK)
async def log_in(
    user_cerd: Annotated[AuthLogin, Form()], 
    response: Response, 
    session: AsyncSession = Depends(get_session)) -> TokenData:
    try:
        refresh_token, access_token = await auth_service.log_in(user_cerd=user_cerd, session=session)
        response.set_cookie(key="refresh-Token", value=refresh_token)
        return access_token
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@auth_router.post('/register', description='Register a new user', status_code=status.HTTP_201_CREATED)
async def sign_up(
    user_cerd: Annotated[AuthSignUp, Form()], 
    response: Response, 
    session: AsyncSession = Depends(get_session)) -> TokenData:

    refresh_token, access_token = await auth_service.sign_up(user_cerd=user_cerd, session=session)
    response.set_cookie(key="refresh-Token", value=refresh_token)
    return access_token


@auth_router.get('/refresh', description='Refresh access token', status_code=status.HTTP_200_OK)
async def refresh_token(
    request: Request,
    response: Response,  
    session: AsyncSession = Depends(get_session)
    ) -> TokenData:

    refresh_token = request.cookies.get('refresh-Token', None)
    try:
       refresh_token, access_token = await auth_service.get_refresh_token(refresh_token, session)
       response.set_cookie(key="refresh-Token", value=refresh_token)
       return access_token
    except NotFoundError as e:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@auth_router.get('/logout', description='Logout user', status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
    valkey_conn: AsyncSession = Depends(get_valkey),
    current_user: AuthUser = Depends(oauth2.get_current_user)
    )-> dict[str, str]:
    
    refresh_token = request.cookies.get('refresh-Token', None)
    try:
       await blacklist_token(refresh_token, valkey_conn, current_user)
    except CredentialsError as e:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return {"detail": "Logged out successfully"}
    
@auth_router.get('/logout-all', description='Logout from all devices', status_code=status.HTTP_200_OK)
async def logout_all(current_user = Depends(oauth2.get_current_user), session: AsyncSession = Depends(get_session)):
    try:
        await auth_service.sign_out_from_all_devices(current_user, session)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"detail": "Logged out from all devices successfully"}
    