from fastapi import APIRouter

from .tag_routers import router as tag_router

router = APIRouter()
router.include_router(tag_router)