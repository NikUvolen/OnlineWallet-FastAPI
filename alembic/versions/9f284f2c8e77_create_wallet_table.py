"""Create wallet table

Revision ID: 9f284f2c8e77
Revises:
Create Date: 2026-06-26 13:19:58.843130

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9f284f2c8e77'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'wallets',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('balance', sa.Numeric(precision=10, scale=2), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('wallets')
