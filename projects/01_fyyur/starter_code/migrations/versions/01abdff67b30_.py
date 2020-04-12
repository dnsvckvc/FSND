"""empty message

Revision ID: 01abdff67b30
Revises: e93b0cf0c594
Create Date: 2020-04-09 21:05:29.840711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01abdff67b30'
down_revision = 'e93b0cf0c594'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue', sa.Integer(), nullable=False),
    sa.Column('artist', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['venue'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    # ### end Alembic commands ###