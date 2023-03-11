from src.models.studants import StudantItem
from src.utils.app_exceptions import AppException, AppExceptionCase
from src.utils.service_results import ServiceResult
from src.utils.session import AppRepositorie, AppService


class StudantRepositorie(AppRepositorie):
    def update_attendence(self, cpf_key: str) -> StudantItem | AppExceptionCase:
        item = self.db.get(cpf_key)
        return item

    def get_studant(self, cpf_key: str) -> StudantItem | AppExceptionCase:
        item = self.db.query((StudantItem)).filter(StudantItem.cpf == cpf_key).all()
        return item


class StudantService(AppService):
    def update_attendence(self, cpf_key: str) -> StudantItem | AppExceptionCase:
        studant_item = StudantRepositorie().update_attendence(cpf_key)
        if not studant_item:
            return ServiceResult(AppException.StudantNotFound())
        return ServiceResult(studant_item)

    def get_studant(self, cpf_key: str) -> StudantItem | AppExceptionCase:
        studant_item = StudantRepositorie().get_studant(cpf_key)
        if not studant_item:
            return ServiceResult(AppException.StudantNotFound())
        return ServiceResult(studant_item)
