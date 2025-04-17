from fastapi import APIRouter

from app.auth import auth_router
from app.tags import tag_router
from app.posts.post_routers import post_router
from app.users.user_routers import user_router

router = APIRouter()
news_router = APIRouter( 
    prefix='/news',
    tags=['news']
    )

news_router.include_router(tag_router)
news_router.include_router(post_router)
news_router.include_router(user_router)

router.include_router(auth_router)
router.include_router(news_router)
