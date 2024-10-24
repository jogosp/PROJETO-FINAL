"""empty message

Revision ID: bcd073d70f55
Revises: 9fdb714ebacf
Create Date: 2024-08-03 11:26:32.477212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcd073d70f55'
down_revision = '9fdb714ebacf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material_recebido', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo_produto', sa.String(), nullable=False))
        batch_op.alter_column('quantidade',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material_recebido', schema=None) as batch_op:
        batch_op.alter_column('quantidade',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.drop_column('tipo_produto')

    # ### end Alembic commands ###
