"""empty message

Revision ID: 463df56e7400
Revises: 41d068234c8a
Create Date: 2017-04-13 12:43:13.268007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '463df56e7400'
down_revision = '41d068234c8a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('public_profiles_blueprint_public_profile', 'img_url', type_=sa.String(length=240))

def downgrade():
    op.alter_column('public_profiles_blueprint_public_profile', 'img_url', type_=sa.String(length=120))
