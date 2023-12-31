"""removed currency in sales statistics model

Revision ID: b19aaf95b190
Revises: eab1444ac7df
Create Date: 2023-11-14 07:43:55.547598

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b19aaf95b190'
down_revision = 'eab1444ac7df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sales_statistics', schema=None) as batch_op:
        batch_op.drop_column('average_price')
        batch_op.drop_column('market_share')
        batch_op.drop_column('total_sales')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sales_statistics', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_sales', mysql.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('market_share', mysql.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('average_price', mysql.FLOAT(), nullable=True))

    # ### end Alembic commands ###
