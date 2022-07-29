"""add user table

Revision ID: 278bea66ef33
Revises: 78be92f9f3ae
Create Date: 2022-07-29 11:38:12.575054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '278bea66ef33'
down_revision = '78be92f9f3ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('uid', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('uid'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
