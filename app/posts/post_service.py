from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_schema import AuthUser
from app.core.schemas import PostCreate, PostWithAuthor
from app.utils.save_image import save_image
from .post_repository import PostRepository


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository
    
    async def get_post(self, session: AsyncSession, post_id: int) -> PostWithAuthor:
        return await self.repository.get_post(session, post_id)

    async def get_posts(self, session: AsyncSession,) -> List[PostWithAuthor]:
        return await self.repository.get_posts(session)

    async def create_post(self, session: AsyncSession, post_in: PostCreate, current_user: AuthUser) -> PostWithAuthor:
        if post_in.image:
            path = save_image(post_in.image.file, current_user.id, post_in.image.filename)
        
        post_in = post_in.model_dump(exclude='image')
        post_in['image'] = path
        return await self.repository.create_post(session, post_in, current_user.id)

    async def delete_post(self, session: AsyncSession, post_id: int) -> bool:
        return await self.repository.delete_post(session, post_id)
