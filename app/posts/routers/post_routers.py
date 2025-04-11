from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.posts import PostRepository, PostService
from app.posts.schemas import PostRead, PostCreate


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

@post_router.post('', status_code=status.HTTP_201_CREATED, response_model=PostRead, description='Create a new post')
async def create_post(post_in: PostCreate, db_session: AsyncSession = Depends(get_session)) -> PostRead:
    return await post_service.create_post(db_session, post_in)

@post_router.delete('/{post_id}')
async def delete_post(post_id: int, db_session:AsyncSession = Depends(get_session)):
    return await post_service.delete_post(db_session, post_id)

