from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.core.schemas import TagCreate, TagRead
from .tag_repository import TagRepository
from .tag_service import TagService


tag_router = APIRouter( 
    prefix='/tags',
    tags=['tags']
    )

tag_service = TagService(repository=TagRepository())

@tag_router.get('', description='Get all tags')
async def get_tags(db_session:AsyncSession = Depends(get_session)) -> List[TagRead]:
    try:
        return await tag_service.get_tags(db_session)
    except NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@tag_router.get('/{tag_id}', description='Get a tag')
async def get_tag(tag_id: int, db_session:AsyncSession = Depends(get_session)) -> TagRead:
    try: 
        return await tag_service.get_tag(db_session, tag_id=tag_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@tag_router.post('', status_code=status.HTTP_201_CREATED, description='Create a new tag')
async def create_tag(tag_in: Annotated[TagCreate, Form()], db_session: AsyncSession = Depends(get_session)) -> TagRead:
    try:
        return await tag_service.create_tag(db_session, tag_in)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
         

@tag_router.delete('/{tag_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, db_session:AsyncSession = Depends(get_session)):
    try:
        await tag_service.delete_tag(db_session, tag_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
         