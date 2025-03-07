from fastapi import APIRouter

from .tag_routers import router as tag_router
from .post_routers import router as post_router

router = APIRouter()
router.include_router(tag_router)
router.include_router(post_router)