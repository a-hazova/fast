from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.tag_schemas import TagRead, TagCreate
from app.repositories.tag_repository import TagRepository
from app.services.tag_service import TagService


router = APIRouter( 
    prefix='/tags',
    tags=['Tags']
    )

tag_service = TagService(repository=TagRepository())

@router.get('', response_model=List[TagRead], description='Get all tags')
async def get_tags(db_session:AsyncSession = Depends(get_session)) -> List[TagRead]:
    return await tag_service.get_tags(db_session)

@router.get('/{tag_id}', response_model=TagRead, description='Get a tag')
async def get_tag(tag_id: int, db_session:AsyncSession = Depends(get_session)) -> TagRead:
    return await tag_service.get_tag(db_session, tag_id=tag_id)

@router.post('', status_code=status.HTTP_201_CREATED, response_model=TagRead, description='Create a new tag')
async def create_tag(tag_in: TagCreate, db_session: AsyncSession = Depends(get_session)) -> TagRead:
    return await tag_service.create_tag(db_session, tag_in)

@router.delete('/{tag_id}')
async def delete_tag(tag_id: int, db_session:AsyncSession = Depends(get_session)):
    return await tag_service.delete_tag(db_session, tag_id)

