import pytest

from datetime import time
from pytest_mock import MockerFixture
from src.models.students_model import Presenca
from src.utils.date_handler import DateHandler
from src.utils.schedule import CourseClass, LateTypes, Schedule
from tests.conftest import ClientContext, DbContext, SeedData


@pytest.mark.integration
class TestPresencaCpfNumber:
    def test_invalid_user_credentials(self, client_context):
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

    def test_attendance_request_not_on_class_time(
        self,
        mocker: MockerFixture,
        client_context: ClientContext,
        seed_db_data: SeedData,
    ):
        client_context.app.dependency_overrides[Schedule] = lambda: mocker.Mock(
            get_current_class=mocker.Mock(return_value=None)
        )

        response = client_context.client.post(
            f"/presenca/{seed_db_data.student.cpf}", auth=client_context.credentials
        )

        response_body = response.json()

        assert response.status_code == 400
        assert response_body["app_exception"] == "NotOngoingLesson"
        assert (
            response_body["message"]
            == "Não há aula em andamento. As presenças só podem ser \
                registradas nos intervalo entre 17:45 até 20:00 e 20:15 até 22:00"
        )

    def test_attendance_already_confirmed(
        self,
        mocker: MockerFixture,
        client_context: ClientContext,
        seed_db_data: SeedData,
    ):
        client_context.app.dependency_overrides[Schedule] = lambda: mocker.Mock(
            get_current_class=lambda: CourseClass(0, time(17, 45), time(20, 00))
        )

        client_context.app.dependency_overrides[DateHandler] = lambda: mocker.Mock(
            is_today=mocker.Mock(return_value=True),
            validate_interval=mocker.Mock(return_value=True),
        )

        response = client_context.client.post(
            f"/presenca/{seed_db_data.student.cpf}", auth=client_context.credentials
        )

        response_body = response.json()

        assert response.status_code == 400
        assert response_body["app_exception"] == "AttendanceAlreadyConfirmed"
        assert response_body["message"] == "Presença já confirmada"

    def test_attendance_successfully_created(
        self,
        mocker: MockerFixture,
        client_context: ClientContext,
        seed_db_data: SeedData,
    ):
        client_context.app.dependency_overrides[Schedule] = lambda: mocker.Mock(
            get_current_class=lambda: CourseClass(0, time(17, 45), time(20, 00))
        )

        client_context.app.dependency_overrides[DateHandler] = lambda: mocker.Mock(
            is_today=mocker.Mock(return_value=False),
            validate_interval=mocker.Mock(return_value=False),
        )

        response = client_context.client.post(
            f"/presenca/{seed_db_data.student.cpf}", auth=client_context.credentials
        )

        assert response.status_code == 201
