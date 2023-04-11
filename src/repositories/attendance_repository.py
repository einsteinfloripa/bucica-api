from fastapi import Depends

from src.database.session import get_db
from src.models.students_model import Presenca
from src.repositories.base_repository import AppRepository
from src.utils.schedule import CourseClass


class AttendanceRepository(AppRepository):
    def create_attendance(self, student_id: int, current_class: CourseClass) -> Presenca:
        created_item = Presenca(
            student_id=student_id,
            late=current_class.is_late(),
            absence=current_class.is_absent(),
            first_half=current_class.is_first_half(),
        )

        self.db.add(created_item)
        self.db.commit()
        self.db.refresh(created_item)

        return created_item

    def get_first_with(self, **kwargs) -> Presenca | None:
        return self.get_first(object=Presenca, **kwargs)
