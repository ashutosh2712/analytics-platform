"""create_widgets_table

Revision ID: cc533cd8a794
Revises: 60b41c8cfa11
Create Date: 2026-06-05 12:48:49.023330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc533cd8a794'
down_revision: Union[str, Sequence[str], None] = '60b41c8cfa11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.create_table(
        "widgets",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "dashboard_id",
            sa.Integer(),
            sa.ForeignKey("dashboards.id"),
            nullable=False,
        ),

        sa.Column(
            "title",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "chart_type",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "metric",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )


def downgrade():

    op.drop_table("widgets")
