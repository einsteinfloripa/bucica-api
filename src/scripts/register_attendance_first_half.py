from datetime import date, datetime
import time
import schedule
from sqlalchemy import func

from src.database.session import SessionLocal
from src.models.students_model import CadastroAlunos, Presenca
from src.utils.schedule import LateTypes
from src.utils.date_handler import DateHandler


def register_attendance():
    if DateHandler().is_holiday(datetime.now()):
        print("Feriado, não serão registradas faltas para o primeiro turno...")
        return

    print("Registrando faltas para o primeiro turno...")
    print("datetime: ", datetime.now())
    db = SessionLocal()

    students = db.query(CadastroAlunos).all()

    for student in students:
        today = date.today()
        last_attendance = (
            db.query(Presenca)
            .filter(
                Presenca.student_id == student.id,
                Presenca.first_half == True,
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


def register_student_first_half():
    schedule.every().monday.at("18:21").do(register_attendance)
    schedule.every().tuesday.at("18:21").do(register_attendance)
    schedule.every().wednesday.at("18:21").do(register_attendance)
    schedule.every().thursday.at("18:21").do(register_attendance)
    schedule.every().friday.at("18:01").do(register_attendance)

    print("Iniciado Job para registar faltas para o primeiro turno...")
    while True:
        schedule.run_pending()
        time.sleep(3)
