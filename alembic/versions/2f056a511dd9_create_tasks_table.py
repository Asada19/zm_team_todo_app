"""create tasks table

Revision ID: 2f056a511dd9
Revises: 7a5a30480ceb
Create Date: 2024-10-02 02:51:29.853051

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2f056a511dd9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True, onupdate=sa.func.now()),
        sa.Column("datetime_to_do", sa.DateTime(), nullable=False),
        sa.Column("task_info", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("tasks")
