from src.models.studants import CadastroAlunos, Presenca
from src.utils.app_exceptions import AppException, AppExceptionCase
from src.utils.calendar import Calendar, CourseClass
from src.utils.service_results import ServiceResult
from src.utils.session import AppRepositorie, AppService


class StudantRepositorie(AppRepositorie):
    def update_attendence(
        self, cpf_key: str, current_class: CourseClass
    ) -> Presenca | AppExceptionCase:
        patent_studant_id = self.get_studant(cpf_key).id

        created_item = Presenca(
            studant_id=patent_studant_id,
            datetime=current_class.start,
            late=current_class.is_late(),
            absence=current_class.is_absencent(),
        )

        self.db.add(created_item)
        self.db.commit()
        self.db.refresh(created_item)

        return created_item

    def get_studant(self, cpf_key: str) -> CadastroAlunos | AppExceptionCase:
        item = (
            self.db.query(CadastroAlunos).filter(CadastroAlunos.cpf == cpf_key).first()
        )
        return item


class StudantService(AppService):
    def update_attendence(self, cpf_key: str) -> Presenca | AppExceptionCase:
        current_class = Calendar().get_current_class()
        if current_class is None:
            return ServiceResult(AppException.ClassNotFound())

        item = StudantRepositorie().update_attendence(cpf_key, current_class)
        if not item:
            return ServiceResult(AppException.StudantNotFound())
        return ServiceResult(item)

    def get_studant(self, cpf_key: str) -> CadastroAlunos | AppExceptionCase:
        studant_item = StudantRepositorie().get_studant(cpf_key)
        if not studant_item:
            return ServiceResult(AppException.StudantNotFound())
        return ServiceResult(studant_item)
