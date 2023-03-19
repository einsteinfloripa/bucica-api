from src.errors.students_exception import (
    AttendanceAlreadyConfirmed,
    NotOngoingLesson,
    StudentNotFound,
)
from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.students_repository import StudentRepository
from src.services.base_services import AppService
from src.utils.schedule import Schedule


class StudentService(AppService):
    student_repository = StudentRepository()
    attendance_repository = AttendanceRepository()
    schedule = Schedule()

    def add_attendance(self, cpf_key: str):
        student = self.student_repository.get_by_cpf(cpf_key)
        if student is None:
            raise StudentNotFound(message="CPF do Aluno não encontrado")

        current_class = self.schedule.get_current_class()
        if current_class is None:
            raise NotOngoingLesson("Não há aula em andamento")

        attendance = self.attendance_repository.get_attendance_by_student_id(student.id)
        if attendance is not None:
            raise AttendanceAlreadyConfirmed("Presença já confirmada")

        self.attendance_repository.create_attendance(student.id, current_class)
