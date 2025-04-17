"""merge heads

Revision ID: 279cf2ea0135
Revises: 18fae522eb77, d2e23d5ba04b
Create Date: 2025-04-17 15:02:22.642823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '279cf2ea0135'
down_revision: Union[str, None] = ('18fae522eb77', 'd2e23d5ba04b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
