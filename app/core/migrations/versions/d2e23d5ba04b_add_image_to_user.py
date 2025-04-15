"""add image to user

Revision ID: d2e23d5ba04b
Revises: 3ff619fe09b5
Create Date: 2025-04-15 15:06:54.679838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2e23d5ba04b'
down_revision: Union[str, None] = '3ff619fe09b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
