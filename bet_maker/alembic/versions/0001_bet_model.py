"""bet model

Revision ID: 0001
Revises: 
Create Date: 2025-01-08 15:15:49.922369

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TYPE bet_status_enum as ENUM('NEW', 'WON', 'LOST');")
    op.create_table(
        "bet",
        sa.Column("event_guid", sa.UUID(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "NEW", "WON", "LOST", name="bet_status_enum", create_type=False
            ),
            server_default="NEW",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("removed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("guid", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("guid"),
    )


def downgrade():
    op.drop_table("bet")
    op.execute("DROP TYPE IF EXISTS bet_status_enum;")
