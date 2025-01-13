"""event model

Revision ID: 0001
Revises: 
Create Date: 2025-01-06 15:15:08.285579

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TYPE event_state_enum as ENUM('NEW', 'FINISHED_WIN', 'FINISHED_LOSE');")
    op.create_table('event',
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('coefficient', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('deadline', sa.Integer(), nullable=False),
    sa.Column('state', postgresql.ENUM('NEW', 'FINISHED_WIN', 'FINISHED_LOSE', name='event_state_enum', create_type=False), server_default='NEW', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('removed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('guid', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('guid')
    )


def downgrade():
    op.drop_table('event')
    op.execute('DROP TYPE IF EXISTS event_state_enum;')