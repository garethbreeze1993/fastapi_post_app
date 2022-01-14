"""add_fk_to_post_table

Revision ID: b197c697658f
Revises: 827007d4f679
Create Date: 2022-01-14 13:21:34.696754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b197c697658f'
down_revision = '827007d4f679'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'],
        ondelete='CASCADE')


def downgrade():
    op.drop_constraint('posts_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
