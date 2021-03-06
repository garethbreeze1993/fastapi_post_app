"""add votes table

Revision ID: 4c54c8cf889f
Revises: 8db97d728973
Create Date: 2022-01-14 13:42:39.217182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c54c8cf889f'
down_revision = '8db97d728973'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='votes_posts_fk', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='votes_users_fk', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
