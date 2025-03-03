from pydantic import BaseModel

from app.models.model import Tag
from app.schemas.base import BaseInDB


class TagCreate(BaseModel):
    name: str

class TagRead(TagCreate):
    id: int
    
    class Config:
        orm_mode = True
    
class TagInDB(BaseInDB, TagCreate):
    
    class Config(BaseInDB.Config):
        orm_model = Tag

