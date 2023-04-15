from datetime import date
import time
import schedule
from sqlalchemy import func

from src.database.session import SessionLocal
from src.models.students_model import CadastroAlunos, Presenca
from src.utils.schedule import LateTypes


@schedule.repeat(schedule.every().monday.tuesday.wednesday.thursday.friday.at("22:00"))
def register_attendance():
    print("Registrando faltas para o segundo turno...")

    db = SessionLocal()

    students = db.query(CadastroAlunos).all()

    for student in students:
        today = date.today()
        last_attendance = (
            db.query(Presenca)
            .filter(
                Presenca.student_id == student.id,
                Presenca.first_half == False,
                func.date(Presenca.created_at) == today,
            )
            .order_by(Presenca.id.desc())
            .first()
        )

        if last_attendance is None:
            new_attendance = Presenca(
                student_id=student.id, first_half=True, absence=True, late=LateTypes.LATE
            )

            db.add(new_attendance)
            db.commit()
            db.refresh(new_attendance)


def register_student_second_half():
    print("Iniciado Job para registar faltas para o segundo turno...")
    while True:
        schedule.run_pending()
        time.sleep(1)
