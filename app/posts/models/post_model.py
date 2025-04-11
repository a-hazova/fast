from datetime import datetime
from typing import List
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base, tag_post_table
from app.tags import Tag

class Post(Base):
    # author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # author: Mapped['User'] = relationship(back_populates = "posts")
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    tags: Mapped[List['Tag']] = relationship(secondary=tag_post_table, lazy='joined', innerjoin=True)
    image: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'
