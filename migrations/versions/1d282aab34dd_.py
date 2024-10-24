"""empty message

Revision ID: 1d282aab34dd
Revises: bcd073d70f55
Create Date: 2024-08-07 21:07:38.562980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d282aab34dd'
down_revision = 'bcd073d70f55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('material_movimentacao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('material_id', sa.Integer(), nullable=False),
    sa.Column('quantidade', sa.Float(), nullable=False),
    sa.Column('destino', sa.String(length=200), nullable=False),
    sa.Column('movimentado_por', sa.String(length=100), nullable=False),
    sa.Column('data_movimentacao', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['material_id'], ['material_recebido.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('post')
    op.drop_table('post_comentarios')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_comentarios',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('data_criacao', sa.DATETIME(), nullable=True),
    sa.Column('comentario', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('post_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('data_criacao', sa.DATETIME(), nullable=True),
    sa.Column('mensagem', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('imagem', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('material_movimentacao')
    # ### end Alembic commands ###
