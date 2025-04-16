from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from fastapi import File, UploadFile
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer

from app.settings import settings

MEDIA_DIR = settings.get_media_dir()

class ImageURLMixin(BaseModel):
    image: Optional[str] = None

    @field_serializer("image")
    def serialize_image(self, value: str | None, _info):
        if not value:
            return None
        relative_path = value.replace("app/", "")
        return f"{settings.BASE_URL}/{relative_path}"

class ImageFormMixin(BaseModel):
    image: Optional[UploadFile] = File(None)


#============Tags==============

class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=127)

    model_config = ConfigDict(from_attributes=True)

class TagRead(TagCreate):
    id: int

#============Posts==============

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=127)
    content: str = Field(min_length=1)
    created_at: Optional[datetime] = None
    tags: str

    model_config = ConfigDict(from_attributes=True)
    
class PostCreateForm(PostBase, ImageFormMixin):
    pass

class PostCreate(PostBase):
    image: Optional[str] = None

class PostRead(PostCreate, ImageURLMixin):
    tags: List[TagRead]

    
class PostWithAuthor(PostRead):
    author: "UserRead"

    @field_serializer('tags', when_used='json', check_fields=False)
    def tags(self, tags: List[TagRead]) -> List[str]:
        return [tag.name for tag in tags]
   
    

#============Users==============
class BaseUser(BaseModel):
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)  

class UserMe(BaseUser, ImageURLMixin):
    id: int
    posts: Optional[List['PostRead']] = None
    password: str
    
class UserUpdateForm(BaseUser, ImageFormMixin):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserRead(BaseUser, ImageURLMixin):
    id: int

class UserWithPosts(UserRead):
    posts: Optional[List['PostRead']] = None



PostWithAuthor.model_rebuild()

 