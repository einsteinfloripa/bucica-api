import pytest

from datetime import datetime
from freezegun import freeze_time
from src.models.students_model import Presenca

from src.repositories.attendance_repository import AttendanceRepository
from src.utils.schedule import (
    CourseClass,
    FirstClassHalf,
    LateTypes,
    SecondClassHalf,
    Weekday,
)
from tests.conftest import ClientContext, DbContext


db_context = DbContext()
db = db_context.session
attendance_repository = AttendanceRepository(db=db)


@pytest.mark.integration
class TestPresencaCpfNumber:
    def test_invalid_user_credentials(self, client_context: ClientContext):
        response = client_context.client.post(
            "/presenca/12345678901", auth=("something", "something")
        )

        response_body = response.json()

        assert response.status_code == 401
        assert response_body["app_exception"] == "NotAuthorized"
        assert response_body["message"] == "Usuário ou senha inválidos"

    def test_student_not_found(self, client_context: ClientContext):
        response = client_context.client.post(
            "/presenca/12345678901", auth=client_context.credentials
        )

        response_body = response.json()

        assert response.status_code == 404
        assert response_body["app_exception"] == "StudentNotFound"
        assert response_body["message"] == "CPF do Aluno não encontrado"

    @freeze_time("2023-04-10 17:40:00")
    def test_attendance_request_not_on_class_time(
        self,
        client_context: ClientContext,
    ):
        response = client_context.client.post(
            f"/presenca/11122233344", auth=client_context.credentials
        )

        response_body = response.json()

        assert response.status_code == 400
        assert response_body["app_exception"] == "NotOngoingLesson"
        assert (
            response_body["message"]
            == "Não há aula em andamento. As presenças só podem ser registradas nos intervalo entre 17:45 até 20:00 e 20:15 até 22:00"
        )

    @freeze_time("2023-04-10 17:45:00")
    def test_attendance_already_confirmed(
        self,
        client_context: ClientContext,
    ):
        attendance_repository.create_attendance(
            student_id=1,
            current_class=CourseClass(
                Weekday.MONDAY.value, FirstClassHalf.BEGIN.value, SecondClassHalf.END.value
            ),
        )

        response = client_context.client.post(
            f"/presenca/11122233344", auth=client_context.credentials
        )

        response_body = response.json()

        assert response.status_code == 400
        assert response_body["app_exception"] == "AttendanceAlreadyConfirmed"
        assert response_body["message"] == "Presença já confirmada"

        db.query(attendance_repository.model).delete()
        db.commit()

    @pytest.mark.parametrize(
        "request_time, expected_response",
        [
            (
                datetime(2023, 4, 10, 17, 55),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 10, 17, 55),
                    "first_half": True,
                },
            ),
            (
                datetime(2023, 4, 10, 20, 25),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 10, 20, 25),
                    "first_half": False,
                },
            ),
            (
                datetime(2023, 4, 11, 17, 55),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 11, 17, 55),
                    "first_half": True,
                },
            ),
            (
                datetime(2023, 4, 11, 20, 25),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 11, 20, 25),
                    "first_half": False,
                },
            ),
            (
                datetime(2023, 4, 12, 17, 55),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 12, 17, 55),
                    "first_half": True,
                },
            ),
            (
                datetime(2023, 4, 12, 20, 25),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 12, 20, 25),
                    "first_half": False,
                },
            ),
            (
                datetime(2023, 4, 13, 17, 55),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 13, 17, 55),
                    "first_half": True,
                },
            ),
            (
                datetime(2023, 4, 13, 20, 25),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 13, 20, 25),
                    "first_half": False,
                },
            ),
            (
                datetime(2023, 4, 14, 17, 55),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 14, 17, 55),
                    "first_half": True,
                },
            ),
            (
                datetime(2023, 4, 14, 20, 25),
                {
                    "status_code": 201,
                    "late": LateTypes.ON_TIME,
                    "absence": False,
                    "created_at": datetime(2023, 4, 14, 20, 25),
                    "first_half": False,
                },
            ),
        ],
    )
    def test_attendance_successfully_created_on_time(
        self,
        client_context: ClientContext,
        request_time: datetime,
        expected_response: dict,
    ):
        with freeze_time(request_time):
            response = client_context.client.post(
                f"/presenca/11122233344", auth=client_context.credentials
            )

        attendance = attendance_repository.get_last_with(student_id=1)

        assert response.status_code == expected_response["status_code"]
        assert attendance.student_id == 1
        assert attendance.late == expected_response["late"]
        assert attendance.absence == expected_response["absence"]
        assert attendance.created_at == expected_response["created_at"]
        assert attendance.first_half == expected_response["first_half"]
