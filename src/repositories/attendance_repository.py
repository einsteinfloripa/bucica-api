from fastapi import Depends
from src.database.session import get_db
from src.models.students_model import Presenca
from src.repositories.base_repository import AppRepository
from src.utils.schedule import CourseClass
from src.database.sheet import Sheet, AttendanceData

class AttendanceRepository(AppRepository):
    def __init__(self, db=Depends(get_db)):
        super().__init__(db, Presenca)

    def create_attendance(self, student_id: int, current_class: CourseClass) -> None:
        presenca = Presenca(
            student_id=student_id,
            late=current_class.is_late(),
            absence=current_class.is_absent(),
            first_half=current_class.is_first_half(),
        )

        self.db.add(presenca)
        self.db.commit()
        self.db.refresh(presenca)

        created_item = self.get_last_with(student_id=student_id)
        Sheet.push_attendance(
            AttendanceData(
                created_item.student_id,
                created_item.first_half,
                created_item.absence,
                created_item.late.value,
                str(created_item.created_at)
            )
        )


    def get_last_with(self, **kwargs) -> Presenca | None:
        return self.get_last(**kwargs)
