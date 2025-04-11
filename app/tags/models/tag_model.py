from sqlalchemy.orm import Mapped, mapped_column

from app.core import Base

class Tag(Base):
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f'<Tag {self.id}: {self.name}>'