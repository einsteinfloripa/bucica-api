from datetime import datetime

from src.models.studants_models import CadastroAlunos, Presenca
from src.repositories.base_repository import AppRepository
from src.utils.app_exceptions import AppExceptionCase
from src.utils.schedule import CourseClass


class StudantRepository(AppRepository):
    def create_attendence(
        self, owner_studant_id: int, current_class: CourseClass
    ) -> Presenca | AppExceptionCase:
        created_item = Presenca(
            studant_id=owner_studant_id,
            datetime_of_creation=datetime.now(),
            late=current_class.is_late(),
            absence=current_class.is_absencent(),
        )

        self.db.add(created_item)
        self.db.commit()
        self.db.refresh(created_item)

        return created_item

    def get_attendence(
        self, studant: CadastroAlunos, current_class: CourseClass
    ) -> Presenca | None:
        return (
            self.db.query(Presenca)
            .filter(
                Presenca.studant_id == studant.id,
                Presenca.datetime == current_class.start,
            )
            .first()
        )

    def get_studant(self, cpf_key: str) -> CadastroAlunos | None:
        return (
            self.db.query(CadastroAlunos).filter(CadastroAlunos.cpf == cpf_key).first()
        )
