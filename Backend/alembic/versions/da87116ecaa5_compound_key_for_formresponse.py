"""Compound key for FormResponse

Revision ID: da87116ecaa5
Revises: 8a4a79e22a0f
Create Date: 2021-08-21 21:34:54.897538

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'da87116ecaa5'
down_revision = '8a4a79e22a0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('formResponses', 'form_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('formResponses', 'form_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###
