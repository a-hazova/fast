from sqlalchemy import Column, ForeignKey, Integer, Table
from app.core.database import Base

tag_post_table = Table(
    'tag_post',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE"), primary_key=True),
    Column('post_id', Integer, ForeignKey('post.id', ondelete="CASCADE"), primary_key=True)

)