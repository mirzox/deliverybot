"""Delivery time added to order

Revision ID: 268c22aa69a9
Revises: 825d5878cecb
Create Date: 2023-04-10 12:32:46.473332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '268c22aa69a9'
down_revision = '825d5878cecb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('delivery_time', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'delivery_time')
    # ### end Alembic commands ###
