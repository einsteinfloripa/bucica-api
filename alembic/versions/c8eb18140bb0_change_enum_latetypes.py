"""change enum 'LateTypes'

Revision ID: c8eb18140bb0
Revises: 788a306aab4d
Create Date: 2023-05-04 06:54:48.348926

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from src.utils.schedule import LateTypes


# revision identifiers, used by Alembic.
revision = "c8eb18140bb0"
down_revision = "788a306aab4d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    late_types = postgresql.ENUM(LateTypes, name="latetypes")
    late_types.create(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    late_types = postgresql.ENUM(LateTypes, name="latetypes")
    late_types.drop(op.get_bind(), checkfirst=True)
