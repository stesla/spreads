"""Initial migration.

Revision ID: 2453e43581c4
Revises: 
Create Date: 2022-06-17 23:06:36.314509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2453e43581c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('social_id', sa.String(), nullable=False),
        sa.Column('given_name', sa.String(), nullable=False),
        sa.Column('family_name', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('social_id')
    )


def downgrade():
    op.drop_table('users')
