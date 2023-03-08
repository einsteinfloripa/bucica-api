from schemas.attendence_schemas import Cpf
from src.models.studants import StudantItem
from utils.session import AppRepositorie, AppService
from src.utils.app_exceptions import AppException, AppExceptionCase
from src.utils.service_results import ServiceResult


class StudantRepositorie(AppRepositorie):
    def update_studant_attendence(self, item: Cpf) -> StudantItem | AppExceptionCase:
        # foo_item = self.db.query(CpfItem).filter(CpfItem.id == item_id).first()

        ### UPDADATE DATABASE

        return item


class StudantService(AppService):
    def update_attendence(self, item: Cpf) -> AppExceptionCase | StudantItem:
        studant_item = StudantRepositorie(self.db).update_studant_attendence(item)
        if not studant_item:
            return ServiceResult(AppException.StudantUpdateAttendance())
        return ServiceResult(studant_item)
