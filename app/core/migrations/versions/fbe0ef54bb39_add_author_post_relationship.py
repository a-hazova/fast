"""add author-post relationship

Revision ID: fbe0ef54bb39
Revises: 6058badbaefd
Create Date: 2025-04-15 10:31:58.214859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbe0ef54bb39'
down_revision: Union[str, None] = '6058badbaefd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
