from datetime import datetime
import time
from typing import List
from sqlalchemy import TIMESTAMP, BigInteger, Column, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


tag_post_table = Table(
    'tag_post',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE"), primary_key=True),
    Column('post_id', Integer, ForeignKey('post.id', ondelete="CASCADE"), primary_key=True)

)

class Tag(Base):
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f'<Tag {self.id}: {self.name}>'

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    image: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str]
    password: Mapped[str] = mapped_column(String(255))
    invalidate_before: Mapped[int] = mapped_column(BigInteger, server_default=text("EXTRACT(EPOCH FROM now())::bigint"))
    posts: Mapped[List["Post"]] = relationship(back_populates="author", lazy="selectin")

    def __repr__(self):
        return f'<User {self.username}, Email: {self.email}>'

class Post(Base):
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped['User'] = relationship(back_populates="posts")
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('now()'))
    tags: Mapped[List['Tag']] = relationship(secondary=tag_post_table, lazy='joined', innerjoin=True)
    image: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'
    