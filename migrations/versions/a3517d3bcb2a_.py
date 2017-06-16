"""empty message

Revision ID: a3517d3bcb2a
Revises: b48f88539d7e
Create Date: 2017-06-09 11:07:16.296388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3517d3bcb2a'
down_revision = 'b48f88539d7e'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('qbo_blueprint_authentication_tokens', 'company_id', type_=sa.BigInteger())

def downgrade():
    op.alter_column('qbo_blueprint_authentication_tokens', 'company_id', type_=sa.Integer())
