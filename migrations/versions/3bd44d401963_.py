"""empty message

Revision ID: 3bd44d401963
Revises: 663f08cba103
Create Date: 2020-06-09 12:43:17.734886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bd44d401963'
down_revision = '663f08cba103'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isbn', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('author', sa.String(length=128), nullable=True),
    sa.Column('publisher_name', sa.String(length=128), nullable=True),
    sa.Column('sales_date', sa.String(length=128), nullable=True),
    sa.Column('image_url', sa.String(length=128), nullable=True),
    sa.Column('donor', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book')
    # ### end Alembic commands ###