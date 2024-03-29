"""donors_table

Revision ID: 762874570ad0
Revises: c8eb18140bb0
Create Date: 2023-07-08 12:53:59.359518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '762874570ad0'
down_revision = 'c8eb18140bb0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Dados_Doador',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('quantidade', sa.Float(), nullable=False),
    sa.Column('indicacao', sa.String(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Dados_Doador')
    # ### end Alembic commands ###
