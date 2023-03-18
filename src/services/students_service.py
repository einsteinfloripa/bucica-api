from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.students_repository import StudentRepository
from src.services.base_services import AppService
from src.utils.app_exceptions import AppException
from src.utils.schedule import Schedule
from src.utils.service_results import ServiceResult


class StudentService(AppService):
    # schedule = Schedule()
    student_repository = StudentRepository()
    attendance_repository = AttendanceRepository()

    def add_attendance(self, cpf_key: str) -> ServiceResult:
        student = self.student_repository.get_by_cpf(cpf_key)
        if student is None:
            return ServiceResult(AppException.StudentNotFound())

        current_class = self.schedule.get_current_class()
        if current_class is None:
            return ServiceResult(AppException.OngoingClassNotFound())

        attendance = self.attendance_repository.get_attendance_by_student_id(student.id)
        if attendance is not None:
            return ServiceResult(AppException.AttendanceAlreadyConfirmed())

        self.attendance_repository.create_attendance(student.id, current_class)
        return ServiceResult()

    def get_student(self, cpf_key: str) -> ServiceResult:
        student_item = self.repository.get_student(cpf_key)
        if student_item is None:
            return ServiceResult(AppException.StudentNotFound())

        return ServiceResult(student_item)
