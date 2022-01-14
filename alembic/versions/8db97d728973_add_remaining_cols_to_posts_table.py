"""add_remaining_cols_to_posts_table

Revision ID: 8db97d728973
Revises: b197c697658f
Create Date: 2022-01-14 13:32:54.810742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8db97d728973'
down_revision = 'b197c697658f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                                     nullable=False))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
