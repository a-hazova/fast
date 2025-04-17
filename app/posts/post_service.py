from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_schema import AuthUser
from app.core.exceptions import NotFoundError
from app.core.models import Post
from app.core.schemas import PostCreate, PostWithAuthor
from app.tags.tag_repository import TagRepository
from app.utils.save_image import save_image
from .post_repository import PostRepository


class PostService:
    def __init__(self, post_repository: PostRepository, tag_repository: TagRepository):
        self.post_repository = post_repository
        self.tag_repository = tag_repository
    
    async def get_post(self, session: AsyncSession, post_id: int) -> Post:
        post = await self.post_repository.get_post(session, post_id)
        if not post:
            raise NotFoundError("Post", "id", post_id)
        return post

    async def get_posts(self, session: AsyncSession,) -> List[Post]:
        posts = await self.post_repository.get_posts(session)
        if not posts:
            raise NotFoundError("Posts")
        return posts

    async def create_post(self, session: AsyncSession, post_data: PostCreate, current_user: AuthUser) -> Post:
        post_dict = post_data.model_dump()

        image = post_dict['image']
        if image:
            path = save_image(image.file, current_user.id, image.filename)
            post_dict['image'] = path

        tag_names = post_dict.pop('tags').split(',')
        existing_tags = await self.tag_repository.get_bulk_tags(session=session, identifier="name", values=tag_names)
        
        existing_tag_names = [tag.name for tag in existing_tags]
        missing_tags = [name for name in tag_names if name not in existing_tag_names]
        if missing_tags:
            raise NotFoundError("Tag", "names", missing_tags)

        return await self.post_repository.create_post(session, post_dict, current_user.id, existing_tags)

    async def delete_post(self, session: AsyncSession, post_id: int) -> bool:
        post = await self.post_repository.get_post(session=session, identifier="id", value=post_id)
        if not post:
            raise NotFoundError("Post", "id", post_id)
        return await self.post_repository.delete_post(session, post)
