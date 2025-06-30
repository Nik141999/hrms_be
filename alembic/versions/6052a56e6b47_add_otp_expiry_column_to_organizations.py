"""Add otp_expiry column to organizations

Revision ID: 6052a56e6b47
Revises: 0a00c5c5dd45
Create Date: 2025-06-26 12:59:36.228455
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6052a56e6b47'
down_revision: Union[str, None] = '0a00c5c5dd45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ✅ ONLY add the new column — don't touch timetracker
    op.add_column('organizations', sa.Column('otp_expiry', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # ✅ Only remove the new column
    op.drop_column('organizations', 'otp_expiry')
