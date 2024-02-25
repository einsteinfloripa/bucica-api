import datetime
import mock
import pytest
import freezegun
import schedule
from src.models.students_model import Presenca
import src.scripts.register_attendance_first_half as first_half
import src.scripts.register_attendance_second_half as second_half
from src.utils.schedule import LateTypes
from src.utils.schedule import CourseClass, FirstClassHalf, Weekday, SecondClassHalf


@pytest.fixture
@freezegun.freeze_time("2023-04-10 00:00:00")  # Monday
def register_mock():
    @schedule.repeat(schedule.every().monday.at("20:01"))
    @schedule.repeat(schedule.every().tuesday.at("20:01"))
    @schedule.repeat(schedule.every().wednesday.at("20:01"))
    @schedule.repeat(schedule.every().thursday.at("20:01"))
    @schedule.repeat(schedule.every().friday.at("20:01"))
    def mocked_register_student_first_half():
        first_half.register_attendance()

    @schedule.repeat(schedule.every().monday.at("22:01"))
    @schedule.repeat(schedule.every().tuesday.at("22:01"))
    @schedule.repeat(schedule.every().wednesday.at("22:01"))
    @schedule.repeat(schedule.every().thursday.at("22:01"))
    @schedule.repeat(schedule.every().friday.at("22:01"))
    def mocked_register_student_second_half():
        second_half.register_attendance()


def insert_attendance(attendance_args, session):
    attendance = Presenca(
        student_id=attendance_args["id"],
        first_half=attendance_args["first_half"],
        absence=attendance_args["absence"],
        late=attendance_args["late"],
    )
    session.add(attendance)
    session.commit()
    session.refresh(attendance)
    return attendance


@pytest.mark.scripts
@pytest.mark.usefixtures("register_mock")
class TestScripts:
    def test_student_absent_in_both_classes(self, session):
        with freezegun.freeze_time("2023-04-10 20:01:01") as frozen_datetime:
            schedule.run_pending()
            frozen_datetime.tick(delta=datetime.timedelta(hours=2))
            schedule.run_pending()

        attendances = session.query(Presenca).filter_by(student_id=1).all()

        first_attendance = attendances[0]
        second_attendance = attendances[1]

        assert first_attendance.absence == True
        assert first_attendance.created_at == datetime.datetime(2023, 4, 10, 20, 1, 1)
        assert first_attendance.first_half == True
        assert first_attendance.late == LateTypes.LATE

        assert second_attendance.absence == True
        assert second_attendance.created_at == datetime.datetime(2023, 4, 10, 22, 1, 1)
        assert second_attendance.first_half == False
        assert second_attendance.late == LateTypes.LATE

    def test_student_absent_in_second_class(self, session, client_context):
        with freezegun.freeze_time("2023-04-10 18:00") as frozen_datetime:
            with mock.patch(
                "src.utils.schedule.Schedule.get_current_class",
                return_value=CourseClass(
                    Weekday.MONDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value
                ),
            ):
                client_context.client.post("/presenca/11122233344", auth=client_context.credentials)
            schedule.run_pending()

            frozen_datetime.tick(
                delta=datetime.timedelta(hours=2, minutes=1, seconds=1)
            )  # 20:01:01
            schedule.run_pending()

            frozen_datetime.tick(delta=datetime.timedelta(hours=2))  # 22:01:01
            schedule.run_pending()

        attendances = session.query(Presenca).filter_by(student_id=1).all()

        first_attendance = attendances[0]
        second_attendance = attendances[1]

        assert first_attendance.absence == False
        assert first_attendance.created_at == datetime.datetime(2023, 4, 10, 18, 0, 0)
        assert first_attendance.first_half == True
        assert first_attendance.late == LateTypes.ON_TIME

        assert second_attendance.absence == True
        assert second_attendance.created_at == datetime.datetime(2023, 4, 10, 22, 1, 1)
        assert second_attendance.first_half == False
        assert second_attendance.late == LateTypes.LATE

    def test_student_absent_in_first_class(self, session, client_context):
        with freezegun.freeze_time("2023-04-10 18:00") as frozen_datetime:
            schedule.run_pending()

            frozen_datetime.tick(
                delta=datetime.timedelta(hours=2, minutes=1, seconds=1)
            )  # 20:01:01
            schedule.run_pending()

            frozen_datetime.tick(delta=datetime.timedelta(minutes=20))  # 20:21:01

            with mock.patch(
                "src.utils.schedule.Schedule.get_current_class",
                return_value=CourseClass(
                    Weekday.MONDAY.value, SecondClassHalf.BEGIN.value, SecondClassHalf.END.value
                ),
            ):
                client_context.client.post("/presenca/11122233344", auth=client_context.credentials)

            frozen_datetime.tick(delta=datetime.timedelta(hours=2))  # 22:01:01
            schedule.run_pending()

        attendances = session.query(Presenca).filter_by(student_id=1).all()

        first_attendance = attendances[0]
        second_attendance = attendances[1]

        assert first_attendance.absence == True
        assert first_attendance.created_at == datetime.datetime(2023, 4, 10, 20, 1, 1)
        assert first_attendance.first_half == True
        assert first_attendance.late == LateTypes.LATE

        assert second_attendance.absence == False
        assert second_attendance.created_at == datetime.datetime(2023, 4, 10, 20, 21, 1)
        assert second_attendance.first_half == False
        assert second_attendance.late == LateTypes.ON_TIME

    def test_student_present_in_both_classes(self, session, client_context):
        with freezegun.freeze_time("2023-04-10 18:00") as frozen_datetime:
            with mock.patch(
                "src.utils.schedule.Schedule.get_current_class",
                return_value=CourseClass(
                    Weekday.MONDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value
                ),
            ):
                client_context.client.post("/presenca/11122233344", auth=client_context.credentials)
            schedule.run_pending()

            frozen_datetime.tick(
                delta=datetime.timedelta(hours=2, minutes=1, seconds=1)
            )  # 20:01:01
            schedule.run_pending()

            frozen_datetime.tick(delta=datetime.timedelta(minutes=20))  # 20:21:01

            with mock.patch(
                "src.utils.schedule.Schedule.get_current_class",
                return_value=CourseClass(
                    Weekday.MONDAY.value, SecondClassHalf.BEGIN.value, SecondClassHalf.END.value
                ),
            ):
                client_context.client.post("/presenca/11122233344", auth=client_context.credentials)

            frozen_datetime.tick(delta=datetime.timedelta(hours=2))  # 22:01:01
            schedule.run_pending()

        attendances = session.query(Presenca).filter_by(student_id=1).all()

        first_attendance = attendances[0]
        second_attendance = attendances[1]

        assert first_attendance.absence == False
        assert first_attendance.created_at == datetime.datetime(2023, 4, 10, 18, 0, 0)
        assert first_attendance.first_half == True
        assert first_attendance.late == LateTypes.ON_TIME

        assert second_attendance.absence == False
        assert second_attendance.created_at == datetime.datetime(2023, 4, 10, 20, 21, 1)
        assert second_attendance.first_half == False
        assert second_attendance.late == LateTypes.ON_TIME

    def test_student_absent_all_week(self, session):
        NUMBER_OF_CLASS_DAYS = 5
        date_times = []
        is_first_half = []
        with freezegun.freeze_time("2023-04-10 20:01:01") as frozen_datetime:
            for _ in range(NUMBER_OF_CLASS_DAYS):
                schedule.run_pending()  # 20:01:01
                date_times.append(datetime.datetime.now())
                is_first_half.append(True)

                frozen_datetime.tick(delta=datetime.timedelta(hours=2))  # 22:01:01
                schedule.run_pending()
                date_times.append(datetime.datetime.now())
                is_first_half.append(False)

                frozen_datetime.tick(delta=datetime.timedelta(days=1, hours=-2))  # 20:01:01

        attendances = session.query(Presenca).filter_by(student_id=1).all()

        for attendance, date_time, first_half in zip(attendances, date_times, is_first_half):
            assert attendance.absence == True
            assert attendance.created_at == date_time
            assert attendance.first_half == first_half
            assert attendance.late == LateTypes.LATE

    # SUPPOSING "2023-04-10 00:00:00" IS A HOLIDAY
    @mock.patch("src.utils.date_handler.DateHandler.is_holiday", return_value=True)
    def test_is_holiday(self, mocked_func, session):
        with freezegun.freeze_time("2023-04-10 20:01:01") as frozen_datetime:
            schedule.run_pending()
            frozen_datetime.tick(delta=datetime.timedelta(hours=2))
            schedule.run_pending()

        attendances = session.query(Presenca).filter_by(student_id=1).all()

        assert len(attendances) == 0
        assert mocked_func.called
