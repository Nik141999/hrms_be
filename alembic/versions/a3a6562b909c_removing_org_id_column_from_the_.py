"""removing org id column from the department table

Revision ID: a3a6562b909c
Revises: d3ad791e0e2f
Create Date: 2025-07-02 12:57:05.368047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a3a6562b909c'
down_revision: Union[str, None] = 'd3ad791e0e2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('departments', 'organization_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('departments', sa.Column('organization_id', mysql.VARCHAR(length=512), nullable=False))
    # ### end Alembic commands ###
