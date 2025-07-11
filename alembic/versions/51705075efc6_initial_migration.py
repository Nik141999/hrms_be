"""Initial migration

Revision ID: 51705075efc6
Revises: 
Create Date: 2025-06-18 12:42:42.346922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '51705075efc6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('department_name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('department_name')
    )
    op.create_table('organization_type',
    sa.Column('id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('org_type', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('org_type')
    )
    op.create_table('roles',
    sa.Column('id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('role_type', sa.String(length=50), nullable=False),
    sa.Column('permission', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_role_type'), 'roles', ['role_type'], unique=True)
    op.create_table('organizations',
    sa.Column('id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('org_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=90), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('phone_number', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('gst_number', mysql.VARCHAR(length=40), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('org_type_id', mysql.VARCHAR(length=512), nullable=True),
    sa.ForeignKeyConstraint(['org_type_id'], ['organization_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('org_name')
    )
    op.create_index(op.f('ix_organizations_email'), 'organizations', ['email'], unique=True)
    op.create_table('users',
    sa.Column('id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('role_id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('organization_id', mysql.VARCHAR(length=512), nullable=True),
    sa.Column('department_id', mysql.VARCHAR(length=512), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=90), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('otp', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('TimeTracker',
    sa.Column('id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('user_id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('punch_in', sa.DateTime(timezone=True), nullable=True),
    sa.Column('punch_out', sa.DateTime(timezone=True), nullable=True),
    sa.Column('duration', sa.String(length=50), nullable=True),
    sa.Column('activity', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('leaves',
    sa.Column('id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('user_id', mysql.VARCHAR(length=512), nullable=False),
    sa.Column('reviewer_id', mysql.VARCHAR(length=512), nullable=True),
    sa.Column('leave_type', sa.String(length=50), nullable=False),
    sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('ACCEPTED', 'REJECTED', 'PENDING', name='leavestatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['reviewer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('leaves')
    op.drop_table('TimeTracker')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_organizations_email'), table_name='organizations')
    op.drop_table('organizations')
    op.drop_index(op.f('ix_roles_role_type'), table_name='roles')
    op.drop_table('roles')
    op.drop_table('organization_type')
    op.drop_table('departments')
    # ### end Alembic commands ###
