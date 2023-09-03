"""Create Tasks table

Revision ID: ef5d72b76e00
Revises: ca01e39f3ebf
Create Date: 2021-08-22 23:19:06.285234

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ef5d72b76e00'
down_revision = 'ca01e39f3ebf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('module', sa.String(), nullable=False),
    sa.Column('func', sa.String(), nullable=False),
    sa.Column('asyncStatus', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    # ### end Alembic commands ###