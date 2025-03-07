from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.schemas.tag_schemas import TagCreate


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=127)
    content: str = Field(min_length=1)
    created_at: datetime = None
    tags: List[str]

    model_config = ConfigDict(from_attributes=True)
    
    

class PostRead(PostCreate):
    id: int
    tags: List[TagCreate]

    @field_serializer('tags', when_used='json')
    def tags(self, values):
        return [tag.name for tag in values]
    


    



