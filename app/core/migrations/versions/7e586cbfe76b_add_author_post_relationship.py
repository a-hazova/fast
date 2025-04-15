"""add author-post relationship

Revision ID: 7e586cbfe76b
Revises: fbe0ef54bb39
Create Date: 2025-04-15 10:35:06.143587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e586cbfe76b'
down_revision: Union[str, None] = 'fbe0ef54bb39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
