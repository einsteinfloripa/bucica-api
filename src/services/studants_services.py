from src.repositories.studants_repository import StudantRepository
from src.services.base_services import AppService
from src.utils.app_exceptions import AppException
from src.utils.schedule import Schedule
from src.utils.service_results import ServiceResult


class StudantService(AppService):
    schedule = Schedule()
    repository = StudantRepository()

    def create_attendence_check(self, cpf_key: str) -> ServiceResult:
        studant = self.repository.get_studant(cpf_key)
        if studant is None:
            return ServiceResult(AppException.StudantNotFound())

        current_class = self.schedule.get_current_class()
        if current_class is None:
            return ServiceResult(AppException.OngoingClassNotFound())

        attendence = self.repository.get_attendence(studant, current_class)

        if attendence is None:
            item = self.repository.create_attendence(studant.id, current_class)
            return ServiceResult(item)
        else:
            return ServiceResult(AppException.AttendanceAlreadyComfimed())

    def get_studant(self, cpf_key: str) -> ServiceResult:
        studant_item = self.repository.get_studant(cpf_key)
        if studant_item is None:
            return ServiceResult(AppException.StudantNotFound())
        return ServiceResult(studant_item)
