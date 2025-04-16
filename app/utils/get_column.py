from typing import Union
from app.core.database import Base


def get_column(entity: Base, identifier: Union[str, int]):
    column = getattr(entity, identifier, None)
    if column is None:
        raise ValueError(f"Invalid field name: {identifier}")
    return column