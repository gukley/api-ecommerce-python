"""add admin_id to users

Revision ID: add_admin_id_to_users
Revises: <coloque o id da última migration aqui>
Create Date: <coloque a data aqui>

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_admin_id_to_users'
down_revision = '<coloque o id da última migration aqui>'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('admin_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_users_admin_id_users',
        'users', 'users',
        ['admin_id'], ['id'],
        ondelete='SET NULL'
    )

def downgrade():
    op.drop_constraint('fk_users_admin_id_users', 'users', type_='foreignkey')
    op.drop_column('users', 'admin_id')
