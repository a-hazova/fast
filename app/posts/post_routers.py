from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import oauth2
from app.auth.auth_schema import AuthUser
from app.core.database import get_session
from app.core.schemas import PostCreate, PostRead
from .post_repository import PostRepository
from .post_service import PostService


post_router = APIRouter( 
    prefix='/posts',
    tags=['posts']
    )

post_service = PostService(repository=PostRepository())

@post_router.get('', response_model=List[PostRead], description='Get all posts')
async def get_posts(db_session:AsyncSession = Depends(get_session)) -> List[PostRead]:
    return await post_service.get_posts(db_session)

@post_router.get('/{post_id}', response_model=PostRead, description='Get a post')
async def get_post(post_id: int, db_session:AsyncSession = Depends(get_session)) -> PostRead:
    return await post_service.get_post(db_session, post_id=post_id)

@post_router.post('', status_code=status.HTTP_201_CREATED, description='Create a new post')
async def create_post(post_in: Annotated[PostCreate, Form()], db_session: AsyncSession = Depends(get_session), current_user: AuthUser = Depends(oauth2.get_current_user)) -> PostRead:
    return await post_service.create_post(db_session, post_in, current_user)

@post_router.delete('/{post_id}')
async def delete_post(post_id: int, db_session:AsyncSession = Depends(get_session)):
    return await post_service.delete_post(db_session, post_id)
