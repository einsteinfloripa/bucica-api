from fastapi import Depends
from src.database.session import get_db
from src.models.students_model import CadastroAlunos
from src.repositories.base_repository import AppRepository


class StudentRepository(AppRepository):
    def __init__(self, db=Depends(get_db)):
        super().__init__(db, CadastroAlunos)

    def get_by_cpf(self, cpf_key: str) -> CadastroAlunos | None:
        return self.get_first(cpf=cpf_key)
