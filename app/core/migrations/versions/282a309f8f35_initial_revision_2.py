"""Initial revision 2

Revision ID: 282a309f8f35
Revises: 577bccc9a262
Create Date: 2025-03-07 14:50:00.067201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '282a309f8f35'
down_revision: Union[str, None] = '577bccc9a262'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tag_post_tag_id_fkey', 'tag_post', type_='foreignkey')
    op.drop_constraint('tag_post_post_id_fkey', 'tag_post', type_='foreignkey')
    op.create_foreign_key(None, 'tag_post', 'post', ['post_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'tag_post', 'tag', ['tag_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tag_post', type_='foreignkey')
    op.drop_constraint(None, 'tag_post', type_='foreignkey')
    op.create_foreign_key('tag_post_post_id_fkey', 'tag_post', 'post', ['post_id'], ['id'])
    op.create_foreign_key('tag_post_tag_id_fkey', 'tag_post', 'tag', ['tag_id'], ['id'])
    # ### end Alembic commands ###
