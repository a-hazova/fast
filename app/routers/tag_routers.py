from fastapi import APIRouter, status, Depends

from app.core.db_service import db_service
from app.core.database import database
from app.models.model import Tag
from app.schemas.tag_schemas import TagCreate, TagInDB, TagRead



router = APIRouter( 
    prefix='/tags',
    tags=['Tags']
    )

@router.post(
        '',
        response_model=TagRead,
        status_code=201,
        description='Create a new tag'
)
async def create_tag(tag_in: TagCreate, db_session=Depends(database.get_session)) -> Tag:
    tag_in = TagInDB(name=tag_in.name)
    return await db_service.create_tag(db_session, tag_in=tag_in)