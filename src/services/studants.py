from src.models.studants import StudantItem
from src.utils.app_exceptions import AppException, AppExceptionCase
from src.utils.service_results import ServiceResult
from src.utils.session import AppRepositorie, AppService


class StudantRepositorie(AppRepositorie):
    def update_studant_attendence(self, cpf_key: str) -> StudantItem | AppExceptionCase:
        # foo_item = self.db.query(CpfItem).filter(CpfItem.id == item_id).first()
        ### UPDADATE DATABASE

        item = self.db.get(cpf_key)

        return item


class StudantService(AppService):
    def update_attendence(self, cpf_key: str) -> AppExceptionCase | StudantItem:
        studant_item = StudantRepositorie().update_studant_attendence(cpf_key)
        if not studant_item:
            return ServiceResult(AppException.StudantNotFound())
        return ServiceResult(studant_item)
