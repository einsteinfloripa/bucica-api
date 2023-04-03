from src.models.students_model import CadastroAlunos
from src.repositories.base_repository import AppRepository


class StudentRepository(AppRepository):
    def get_by_cpf(self, cpf_key: str) -> CadastroAlunos | None:
        return self.get_first(object=CadastroAlunos, cpf=cpf_key)
