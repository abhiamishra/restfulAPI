"""add content column to posts table

Revision ID: 78be92f9f3ae
Revises: 74e59c0387c9
Create Date: 2022-07-29 11:24:26.982665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78be92f9f3ae'
down_revision = '74e59c0387c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
