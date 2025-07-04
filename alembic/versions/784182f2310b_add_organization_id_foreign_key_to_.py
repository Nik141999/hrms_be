"""Add organization_id foreign key to department

Revision ID: 784182f2310b
Revises: a3a6562b909c
Create Date: 2025-07-02 13:10:09.419471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '784182f2310b'
down_revision: Union[str, None] = 'a3a6562b909c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('departments', sa.Column('organization_id', mysql.VARCHAR(length=512), nullable=True))
    op.create_foreign_key(None, 'departments', 'organizations', ['organization_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'departments', type_='foreignkey')
    op.drop_column('departments', 'organization_id')
    # ### end Alembic commands ###
