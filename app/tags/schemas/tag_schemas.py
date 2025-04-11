from pydantic import BaseModel, ConfigDict, Field

class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=127)

    model_config = ConfigDict(from_attributes=True)

class TagRead(TagCreate):
    id: int

