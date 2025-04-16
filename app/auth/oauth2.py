
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

from app.settings import settings
from app.users.user_repository import UserRepository
from .auth_schema import Token, AuthUser
from app.core.database import get_session


SECRET_KEY = settings.SECRET_KEY
ALGORITHM =  settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

repository: UserRepository = UserRepository

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta: 
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = str(payload.get("user_id"))
        if id is None:
            raise credentials_exception
        token_data = Token(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session))-> AuthUser:
        
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                              detail="Could not validate credentials", headers={"WWW-Authenticare": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user =  await repository.get_user(user_id=token.id, session=session)
    return user

