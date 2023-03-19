from src.models.students_model import CadastroAlunos
from src.repositories.base_repository import DBSessionMixin


class StudentRepository(DBSessionMixin):
    def get_by_cpf(self, cpf_key: str) -> CadastroAlunos | None:
        return self.db.query(CadastroAlunos).filter(CadastroAlunos.cpf == cpf_key).first()
