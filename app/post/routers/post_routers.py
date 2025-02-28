from fastapi import APIRouter, Depends
from app.core.database import database
from app.post.models import Post
from app.post.post_schema import PostSchema



router = APIRouter()

@router.post("/posts")
async def create_post(post_data: PostSchema, db_session=Depends(database.get_session)):
    pass