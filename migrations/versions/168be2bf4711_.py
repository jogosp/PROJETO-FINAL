"""empty message

Revision ID: 168be2bf4711
Revises: 0a8bf02ee0be
Create Date: 2024-07-04 09:39:53.346191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '168be2bf4711'
down_revision = '0a8bf02ee0be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('usuario', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('cargo', sa.String(), nullable=True))
        batch_op.drop_column('nome')
        batch_op.drop_column('sobrenome')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sobrenome', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('nome', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('cargo')
        batch_op.drop_column('usuario')

    # ### end Alembic commands ###
