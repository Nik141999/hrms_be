"""Changing column length

Revision ID: 6d8e417cc8d4
Revises: 563624693eb9
Create Date: 2025-07-02 15:39:12.039188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '6d8e417cc8d4'
down_revision: Union[str, None] = '563624693eb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('organizations', 'id',
               existing_type=mysql.VARCHAR(length=512),
               type_=mysql.VARCHAR(length=36),
               existing_nullable=False)
    op.alter_column('organizations', 'org_name',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=20),
               existing_nullable=False)
    op.alter_column('organizations', 'email',
               existing_type=mysql.VARCHAR(length=90),
               type_=sa.String(length=120),
               existing_nullable=True)
    op.alter_column('organizations', 'role_id',
               existing_type=mysql.VARCHAR(length=512),
               type_=mysql.VARCHAR(length=36),
               existing_nullable=False)
    op.alter_column('organizations', 'org_type_id',
               existing_type=mysql.VARCHAR(length=512),
               type_=mysql.VARCHAR(length=36),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('organizations', 'org_type_id',
               existing_type=mysql.VARCHAR(length=36),
               type_=mysql.VARCHAR(length=512),
               existing_nullable=True)
    op.alter_column('organizations', 'role_id',
               existing_type=mysql.VARCHAR(length=36),
               type_=mysql.VARCHAR(length=512),
               existing_nullable=False)
    op.alter_column('organizations', 'email',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=90),
               existing_nullable=True)
    op.alter_column('organizations', 'org_name',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
    op.alter_column('organizations', 'id',
               existing_type=mysql.VARCHAR(length=36),
               type_=mysql.VARCHAR(length=512),
               existing_nullable=False)
    # ### end Alembic commands ###
