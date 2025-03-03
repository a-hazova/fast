from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, RelationshipProperty
from sqlalchemy.ext.asyncio import AsyncAttrs

from .base import Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    # tags = Column(String, ForeignKey('tag.name'), nullable=False)
    # author: RelationshipProperty = relationship("Author", backref = "posts")

class Tag(Base, AsyncAttrs):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class PostTag(Base):
    __tablename__ = 'posttag'

    post_id = Column(
        Integer,
        ForeignKey('post.id', ondelete='CASCADE'), primary_key=True
    )
    category_id = Column(
        Integer,
        ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True
    )    
