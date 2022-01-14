"""add_user_table

Revision ID: 827007d4f679
Revises: e7b59e4a98f9
Create Date: 2022-01-14 13:07:48.204360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '827007d4f679'
down_revision = 'e7b59e4a98f9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')
