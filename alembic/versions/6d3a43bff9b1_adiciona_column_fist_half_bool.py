"""adiciona column 'fist_half': bool

Revision ID: 6d3a43bff9b1
Revises: 0c3b7d8a51ab
Create Date: 2023-03-20 20:19:28.596324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d3a43bff9b1'
down_revision = '0c3b7d8a51ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Presenca', sa.Column('primeira_metade', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Presenca', 'primeira_metade')
    # ### end Alembic commands ###