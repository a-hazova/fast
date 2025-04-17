
from typing import Literal
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import CredentialsError
from app.settings import settings
from app.users.user_repository import UserRepository
from .auth_schema import Token, AuthUser
from app.core.database import get_session, get_valkey


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_SECRET_KEY = settings.REFRESH_TOKEN_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

repository: UserRepository = UserRepository


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(minutes=eval(REFRESH_TOKEN_EXPIRE_MINUTES))):
    to_encode = data.copy()
    creation_time = datetime.now(timezone.utc)
    expire = creation_time + expires_delta

    to_encode.update({
        'exp': expire,
        'created': creation_time.timestamp()
        })
    
    encoded_jwt = jwt.encode(
        to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, type: Literal['access', 'refresh'] = 'access'):
    try:
        if type == 'access':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        else:
            payload = jwt.decode(
                token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = payload    
        if token_data is None:
            raise CredentialsError()
    except InvalidTokenError:
        raise CredentialsError()
    return token_data

async def verify_refresh_token(token, session: AsyncSession = None, invalidate_before: int = None ):
    token_data = verify_token(token, type='refresh')
    valkey_conn = await get_valkey()
    is_blacklisted = await valkey_conn.get(token)

    token_timestamp = int(token_data['created'])
    if not invalidate_before:
        user = await repository.get_user(identifier="id", value=int(token_data['sub']), session=session)
        invalidate_before = user.invalidate_before

    is_expired = token_timestamp < invalidate_before
        
    if is_blacklisted or is_expired:
        raise HTTPException(status_code=401, detail="Token has been expired")
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> AuthUser:
    try: 
        token_data = verify_token(token)
        user = await repository.get_user(identifier="id", value=int(token_data['sub']), session=session)
        
        return user
    except CredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

async def blacklist_token(token: str, valkey_conn, current_user: AuthUser) -> bool:
        token_data = await verify_refresh_token(token=token, invalidate_before=current_user.invalidate_before)
        exp = token_data['exp']

        now_ts = int(datetime.now(timezone.utc).timestamp())
        tte = exp - now_ts
        if tte > 0:
            await valkey_conn.setex(token, tte, "1")
        return True

