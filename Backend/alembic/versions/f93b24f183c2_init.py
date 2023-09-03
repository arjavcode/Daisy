"""init

Revision ID: f93b24f183c2
Revises: 
Create Date: 2021-08-20 23:43:50.196060

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f93b24f183c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forms',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=False),
    sa.Column('desc', sa.String(length=300), nullable=True),
    sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('question_text', sa.String(), nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('formQuestions',
    sa.Column('form_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('question_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('question_order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('form_id', 'question_id'),
    sa.UniqueConstraint('form_id', 'question_order')
    )
    op.create_table('formResponses',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('form_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('responded_on', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('responses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('question_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('response', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'question_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('responses')
    op.drop_table('formResponses')
    op.drop_table('formQuestions')
    op.drop_table('questions')
    op.drop_table('forms')
    # ### end Alembic commands ###
