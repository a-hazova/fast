from fastapi import APIRouter

from app.tags import tag_router
from app.posts import post_router

router = APIRouter()
router.include_router(tag_router)
router.include_router(post_router)