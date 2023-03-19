from datetime import datetime

from src.models.students_model import Presenca
from src.repositories.base_repository import AppRepository
from src.utils.schedule import CourseClass


class AttendanceRepository(AppRepository):
    def create_attendance(self, student_id: int, current_class: CourseClass) -> Presenca:
        created_item = Presenca(
            student_id=student_id,
            late=current_class.is_late(),
            absence=current_class.is_absent(),
        )

        self.db.add(created_item)
        self.db.commit()
        self.db.refresh(created_item)

        return created_item

    def get_attendance_by_student_id(self, student_id: int) -> Presenca | None:
        return (
            self.db.query(Presenca)
            .filter(
                Presenca.student_id == student_id,
                Presenca.created_at == datetime.now().date(),
            )
            .first()
        )
