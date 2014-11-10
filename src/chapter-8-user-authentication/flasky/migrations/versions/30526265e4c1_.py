"""empty message

Revision ID: 30526265e4c1
Revises: 24bbe4dbf603
Create Date: 2014-11-10 16:42:29.686921

"""

# revision identifiers, used by Alembic.
revision = '30526265e4c1'
down_revision = '24bbe4dbf603'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    ### end Alembic commands ###
