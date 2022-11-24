"""merging two heads

Revision ID: 25e177652076
Revises: 20c279fe2e04, dd66d437cc20
Create Date: 2022-11-23 21:49:53.004846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25e177652076'
down_revision = ('20c279fe2e04', 'dd66d437cc20')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
