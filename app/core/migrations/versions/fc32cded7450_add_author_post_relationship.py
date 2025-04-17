"""add author-post relationship

Revision ID: fc32cded7450
Revises: 7e586cbfe76b
Create Date: 2025-04-15 10:39:53.556645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc32cded7450'
down_revision: Union[str, None] = '7e586cbfe76b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
