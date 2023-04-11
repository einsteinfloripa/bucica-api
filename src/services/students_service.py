from fastapi import Depends

from src.errors.students_exception import (AttendanceAlreadyConfirmed,
                                           NotOngoingLesson, StudentNotFound)
from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.students_repository import StudentRepository
from src.utils.schedule import Schedule


class StudentService:
    def __init__(
        self,
        student_repository: StudentRepository = Depends(StudentRepository),
        attendance_repository: AttendanceRepository = Depends(AttendanceRepository),
        schedule: Schedule = Depends(Schedule),
    ):
        self.student_repository = student_repository
        self.attendance_repository = attendance_repository
        self.schedule = schedule

    def add_attendance(self, cpf_key: str):
        student = self.student_repository.get_by_cpf(cpf_key)
        if student is None:
            raise StudentNotFound("CPF do Aluno não encontrado")

        current_class = self.schedule.get_current_class()
        if current_class is None:
            raise NotOngoingLesson("Não há aula em andamento")

        attendance = self.attendance_repository.get_first_with(
            student_id=student.id, first_half=current_class.is_first_half()
        )
        if attendance is not None:
            raise AttendanceAlreadyConfirmed("Presença já confirmada")

        self.attendance_repository.create_attendance(student.id, current_class)
