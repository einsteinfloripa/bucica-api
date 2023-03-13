"""add_mock_data

Revision ID: 856757bd0ae7
Revises: 2d6b10cfcb5d
Create Date: 2023-03-12 22:36:35.806474

"""
from datetime import date, datetime

import sqlalchemy as sa

from alembic import op
from src.models.studants import CadastroAlunos, Presenca

# revision identifiers, used by Alembic.
revision = "856757bd0ae7"
down_revision = "2d6b10cfcb5d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        CadastroAlunos.__table__,
        [
            {
                "id": 1,
                "name": "John Doe",
                "phone": "5511223344",
                "birthdate": date(1990, 1, 1),
                "rg": "123456789",
                "cpf": "12345678901",
                "civil_state": "casado",
                "state": "SC",
                "city": "florianopolis",
                "neighborhood": "trindade",
                "street": "rua 15",
                "number": "222",
                "complement": "perto de nada",
                "cep": "88033404",
                "email": "john.doe@gmail.com",
            }
        ],
    )
    op.bulk_insert(
        Presenca.__table__,
        [
            {
                "id": 1,
                "studant_id": 1,
                "datetime": datetime(2021, 1, 1, 0, 0),
                "late": 1,
                "absence": False,
            },
            {
                "id": 2,
                "studant_id": 1,
                "datetime": datetime(2021, 1, 2, 0, 0),
                "late": 1,
                "absence": False,
            },
        ],
    )


def downgrade() -> None:
    op.execute('DELETE FROM "Presenca"')
    op.execute('DELETE FROM "Cadastro_Alunos"')
