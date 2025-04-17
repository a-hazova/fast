from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import oauth2
from app.auth.auth_schema import AuthUser
from app.core.database import get_session
from app.core.exceptions import NotFoundError
from app.core.schemas import PostCreateForm, PostWithAuthor
from app.tags.tag_repository import TagRepository
from .post_repository import PostRepository
from .post_service import PostService


post_router = APIRouter( 
    prefix='/posts',
    tags=['posts']
    )

post_service = PostService(post_repository=PostRepository(), tag_repository=TagRepository)

@post_router.get('', description='Get all posts')
async def get_posts(db_session:AsyncSession = Depends(get_session)) -> List[PostWithAuthor]:
    try:
        return await post_service.get_posts(db_session)
    except NotFoundError as e: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@post_router.get('/{post_id}', description='Get a post')
async def get_post(post_id: int, db_session:AsyncSession = Depends(get_session)) -> PostWithAuthor:
    try:
        return await post_service.get_post(db_session, post_id=post_id)
    except NotFoundError as e: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@post_router.post('', status_code=status.HTTP_201_CREATED, description='Create a new post')
async def create_post(
    post_in: Annotated[PostCreateForm, Form(media_type="multipart/form-data")], 
    db_session: AsyncSession = Depends(get_session), 
    current_user: AuthUser = Depends(oauth2.get_current_user)
    ) -> PostWithAuthor:
    try: 
        return await post_service.create_post(db_session, post_in, current_user)
    except NotFoundError as e: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        
@post_router.delete('/{post_id}')
async def delete_post(post_id: int, db_session:AsyncSession = Depends(get_session)):
    try: 
        return await post_service.delete_post(db_session, post_id)
    except NotFoundError as e: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
