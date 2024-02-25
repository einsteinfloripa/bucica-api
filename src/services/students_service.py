from datetime import datetime
from fastapi import Depends


from src.errors.students_exception import (
    AttendanceAlreadyConfirmed,
    NotOngoingClass,
    StudentNotFound,
)
from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.students_repository import StudentRepository
from src.utils.date_handler import DateHandler
from src.utils.schedule import Schedule, FirstClassHalf, SecondClassHalf


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
            raise NotOngoingClass(
                f"Não há aula em andamento. As presenças só podem ser registradas nos intervalo entre \
{FirstClassHalf.begin_time_str()} até {FirstClassHalf.end_time_str()} e \
{SecondClassHalf.begin_time_str()} até {SecondClassHalf.end_time_str()}"
            )

        attendance = self.attendance_repository.get_last_with(student_id=student.id)

        if attendance is not None:
            is_attendance_class_ongoing = self.date_handler.between(
                attendance.created_at, current_class.start, current_class.end
            )
            if is_attendance_class_ongoing:
                raise AttendanceAlreadyConfirmed("Presença já confirmada")

        self.attendance_repository.create_attendance(student.id, current_class)
