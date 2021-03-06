"""empty message

Revision ID: fc910bdfa369
Revises: c9abe193eb19
Create Date: 2020-04-13 13:20:51.642801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc910bdfa369'
down_revision = 'c9abe193eb19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('shows_venue_fkey', 'shows', type_='foreignkey')
    op.drop_constraint('shows_artist_fkey', 'shows', type_='foreignkey')
    op.create_foreign_key(None, 'shows', 'venues', ['venue'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'shows', 'artists', ['artist'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.create_foreign_key('shows_artist_fkey', 'shows', 'artists', ['artist'], ['id'])
    op.create_foreign_key('shows_venue_fkey', 'shows', 'venues', ['venue'], ['id'])
    # ### end Alembic commands ###
