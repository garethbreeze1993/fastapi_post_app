"""add_content_to post_table

Revision ID: e7b59e4a98f9
Revises: 4c21b114e175
Create Date: 2022-01-14 12:36:02.419038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7b59e4a98f9'
down_revision = '4c21b114e175'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
