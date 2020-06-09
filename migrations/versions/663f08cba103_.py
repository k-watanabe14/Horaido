"""empty message

Revision ID: 663f08cba103
Revises: a8ce34429a4d
Create Date: 2020-06-09 12:41:27.830098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '663f08cba103'
down_revision = 'a8ce34429a4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('image_url', sa.String(length=128), nullable=True))
    op.drop_column('book', 'medium_image_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('medium_image_url', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_column('book', 'image_url')
    # ### end Alembic commands ###
