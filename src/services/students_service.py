from fastapi import Depends

from src.errors.students_exception import (
    AttendanceAlreadyConfirmed,
    NotOngoingLesson,
    StudentNotFound,
)
from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.students_repository import StudentRepository
from src.utils.date_handler import DateHandler
from src.utils.schedule import Schedule


class StudentService:
    def __init__(
        self,
        student_repository: StudentRepository = Depends(StudentRepository),
        attendance_repository: AttendanceRepository = Depends(AttendanceRepository),
        schedule: Schedule = Depends(Schedule),
        date_handler: DateHandler = Depends(DateHandler),
    ):
        self.student_repository = student_repository
        self.attendance_repository = attendance_repository
        self.schedule = schedule
        self.date_handler = date_handler

    def add_attendance(self, cpf_key: str):
        student = self.student_repository.get_by_cpf(cpf_key)
        if student is None:
            raise StudentNotFound("CPF do Aluno não encontrado")

        current_class = self.schedule.get_current_class()
        if current_class is None:
            raise NotOngoingLesson(
                "Não há aula em andamento. As presenças só podem ser \
                registradas nos intervalo entre 17:45 até 20:00 e 20:15 até 22:00"
            )

        attendance = self.attendance_repository.get_last_with(student_id=student.id)

        # TODO: Arrumar attendance quando for None e remover o mypy: ignore
        is_today = self.date_handler.is_today(attendance.created_at)  # mypy: ignore
        is_first_half = self.date_handler.validate_interval(
            attendance.created_at, current_class.start, current_class.end  # mypy: ignore
        )
        if is_today and is_first_half:
            raise AttendanceAlreadyConfirmed("Presença já confirmada")

        self.attendance_repository.create_attendance(student.id, current_class)
