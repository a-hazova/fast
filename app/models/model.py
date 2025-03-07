from datetime import datetime
from typing import List
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

tag_post_table = Table(
    'tag_post',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE"), primary_key=True),
    Column('post_id', Integer, ForeignKey('post.id', ondelete="CASCADE"), primary_key=True)

)
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
    
# class User(Base):
#     name: Mapped[str] = mapped_column(nullable=False)
#     email: Mapped[str] = mapped_column(nullable=False)
#     posts: Mapped[List['Post']] = relationship(back_populates = "author", cascade="all, delete-orphans")

#     def __repr__(self):
#         return f'<Author {self.id}: {self.name}>'

class Tag(Base):
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f'<Tag {self.id}: {self.name}>'
