"""initial migration | added value to statistics table

Revision ID: 735c324b3146
Revises: 
Create Date: 2023-11-13 02:44:45.374288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '735c324b3146'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sales_statistics', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stat_value', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sales_statistics', schema=None) as batch_op:
        batch_op.drop_column('stat_value')

    # ### end Alembic commands ###
