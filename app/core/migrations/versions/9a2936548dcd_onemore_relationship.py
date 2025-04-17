"""onemore relationship

Revision ID: 9a2936548dcd
Revises: bca481340522
Create Date: 2025-04-15 10:47:51.582585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a2936548dcd'
down_revision: Union[str, None] = 'bca481340522'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
