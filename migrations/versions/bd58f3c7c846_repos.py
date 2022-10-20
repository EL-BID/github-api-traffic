"""repos

Revision ID: bd58f3c7c846
Revises: af4852a7b14d
Create Date: 2022-10-20 12:30:03.847284

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bd58f3c7c846'
down_revision = 'af4852a7b14d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clones')
    op.drop_table('traffic')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('traffic',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('clone_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('clone_count_unique', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='traffic_pkey')
    )
    op.create_table('clones',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('uniques', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='clones_pkey')
    )
    # ### end Alembic commands ###
