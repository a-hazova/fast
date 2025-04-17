"""another user-post

Revision ID: bca481340522
Revises: fc32cded7450
Create Date: 2025-04-15 10:41:14.989019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bca481340522'
down_revision: Union[str, None] = 'fc32cded7450'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
