from typing import Optional, Type
from pydantic import BaseModel


class BaseInDB(BaseModel):
    # base schema for every schema that stored in DB.
    # provides a default method for converting
    # Pydantic objects to SQLAlchemy objects

    class Config:
        orm_model: Optional[Type[Base]] = None

    def to_orm(self) -> Base:
        if not self.Config.orm_model:
            raise AttributeError("Class not defined Config.orm_model") 
        
        return self.Config.orm_model(**dict(self))

class BaseUpdateInDB(BaseInDB):
    id: int