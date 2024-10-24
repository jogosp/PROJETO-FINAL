"""empty message

Revision ID: 71bc8f83d7b3
Revises: 1d282aab34dd
Create Date: 2024-08-07 21:28:44.154128

"""
# migrations/versions/71bc8f83d7b3_.py

from alembic import op
import sqlalchemy as sa

# Revisão anterior e informações de cabeçalho
revision = '71bc8f83d7b3'
down_revision = '1d282aab34dd'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('material_movimentacao') as batch_op:
        batch_op.add_column(sa.Column('nome_produto', sa.String(length=255), nullable=True))

    # Atualizar registros existentes com um valor padrão
    op.execute('UPDATE material_movimentacao SET nome_produto = "Desconhecido" WHERE nome_produto IS NULL')

    with op.batch_alter_table('material_movimentacao') as batch_op:
        batch_op.alter_column('nome_produto', existing_type=sa.String(length=255), nullable=False)

def downgrade():
    with op.batch_alter_table('material_movimentacao') as batch_op:
        batch_op.drop_column('nome_produto')


