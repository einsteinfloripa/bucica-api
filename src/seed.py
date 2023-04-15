from pytest import Session
from sqlalchemy import Date, Integer, String, column, table

from src.models.students_model import CadastroAlunos


class CadastroAlunosSeed(CadastroAlunos):
    def create_table(self):
        return table(
            "Cadastro_Alunos",
            column("id", Integer),
            column("rg", String),
            column("cpf", String),
            column("cep", String),
            column("email", String),
            column("nome", String),
            column("telefone", String),
            column("data_nascimento", Date),
            column("estado_civil", String),
            column("estado", String),
            column("cidade", String),
            column("bairro", String),
            column("rua", String),
            column("numero", String),
            column("complemento", String),
        )

    def seed(self):
        return [
            {
                "id": 1,
                "rg": self.rg,
                "cpf": self.cpf,
                "cep": self.cep,
                "email": self.email,
                "nome": self.name,
                "telefone": self.phone,
                "data_nascimento": self.birthdate,
                "estado_civil": self.civil_state,
                "estado": self.state,
                "cidade": self.city,
                "bairro": self.neighborhood,
                "rua": self.street,
                "numero": self.number,
                "complemento": self.complement,
            }
        ]
