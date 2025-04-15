from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer



class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=127)

    model_config = ConfigDict(from_attributes=True)

class TagRead(TagCreate):
    id: int
    
class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=127)
    content: str = Field(min_length=1)
    created_at: Optional[datetime] = None
    tags: List[str]

    model_config = ConfigDict(from_attributes=True)
    
class PostInDB(PostCreate):
    author_id: int

class PostRead(PostInDB):
    id: int
    tags: List[TagCreate]
    author: "BaseUser"

    @field_serializer('tags', when_used='json')
    def tags(self, values):
        return [tag.name for tag in values]
    model_config = ConfigDict(from_attributes=True)


class BaseUser(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserRead(BaseUser):
    posts: Optional['PostRead']
    model_config = ConfigDict(from_attributes=True)     


    




 