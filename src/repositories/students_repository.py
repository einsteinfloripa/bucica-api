from datetime import datetime

from src.models.students_model import CadastroAlunos, Presenca
from src.repositories.base_repository import AppRepository
from src.utils.app_exceptions import AppExceptionCase
from src.utils.schedule import CourseClass


class StudentRepository:
    def create_attendance(
        self, owner_student_id: int, current_class: CourseClass
    ) -> Presenca | AppExceptionCase:
        created_item = Presenca(
            student_id=owner_student_id,
            datetime_of_creation=datetime.now(),
            late=current_class.is_late(),
            absence=current_class.is_absent(),
        )

        self.db.add(created_item)
        self.db.commit()
        self.db.refresh(created_item)

        return created_item

    def get_by_cpf(self, cpf_key: str) -> CadastroAlunos | None:
        return (
            self.db.query(CadastroAlunos).filter(CadastroAlunos.cpf == cpf_key).first()
        )
