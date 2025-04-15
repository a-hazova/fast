from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.schemas import TagCreate, TagRead
from .tag_repository import TagRepository
from .tag_service import TagService


tag_router = APIRouter( 
    prefix='/tags',
    tags=['tags']
    )

tag_service = TagService(repository=TagRepository())

@tag_router.get('', response_model=List[TagRead], description='Get all tags')
async def get_tags(db_session:AsyncSession = Depends(get_session)) -> List[TagRead]:
    return await tag_service.get_tags(db_session)

@tag_router.get('/{tag_id}', response_model=TagRead, description='Get a tag')
async def get_tag(tag_id: int, db_session:AsyncSession = Depends(get_session)) -> TagRead:
    return await tag_service.get_tag(db_session, tag_id=tag_id)

@tag_router.post('', status_code=status.HTTP_201_CREATED, response_model=TagRead, description='Create a new tag')
async def create_tag(tag_in: Annotated[TagCreate, Form()], db_session: AsyncSession = Depends(get_session)) -> TagRead:
    return await tag_service.create_tag(db_session, tag_in)

@tag_router.delete('/{tag_id}')
async def delete_tag(tag_id: int, db_session:AsyncSession = Depends(get_session)):
    return await tag_service.delete_tag(db_session, tag_id)

