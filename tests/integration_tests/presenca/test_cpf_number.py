from ast import Tuple
import datetime
from turtle import width
import mock
import pytest

from datetime import time
from freezegun import freeze_time
from pytest_mock import MockerFixture
from sqlalchemy import true
from src.models.students_model import CadastroAlunos, Presenca
from src.repositories.attendance_repository import AttendanceRepository
from src.utils.date_handler import DateHandler
from src.utils.schedule import CourseClass, LateTypes, Schedule
from tests.conftest import ClientContext, DbContext, SeedData, db_context
from src.repositories.students_repository import AppRepository




def seed_presenca(db: DbContext, _student_id: int, creation_time: datetime.datetime, _late: bool, _absence: bool, _first_half: bool):

    with freeze_time(creation_time) as mocked_time:
        item = Presenca(
            student_id=_student_id,
            late=_late,
            absence=_absence,
            first_half=_first_half,
        )
    
    db.add(item)
    db.commit()
    db.refresh(item)




@pytest.mark.integration
class TestPresencaCpfNumber:

    PRESENCAS = []

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

    @pytest.mark.t
    @pytest.mark.parametrize(
            "current_class_args, seed_presencas_args, is_today, validate_interval, request_time, expected_response",
            [
                (
                    (1, time(17, 45), time(20, 00)),
                    [],
                    True,
                    True,
                    datetime.datetime(2023,4,11,17,55),
                    {
                        "status_code":201, 
                        "late": LateTypes.ON_TIME, 
                        "absence": False, 
                        "created_at": datetime.datetime(2023,4,11,17,55), "first_half": True}
                ),
                (
                    (0, time(17, 45), time(20, 00)),
                    [()],
                    True,
                    True,
                    datetime.datetime(2023,4,10,18,5),
                    {
                        "status_code":201,
                        "late": LateTypes.LATE,
                        "absence": False,
                        "created_at": datetime.datetime(2023,4,10,18,5),
                        "first_half": True,
                    },
                ),
            ],
    )
    def test_attendance_successfully_created(
        self,
        mocker: MockerFixture,
        client_context: ClientContext,
        db_context: DbContext,
        seed_db_data: SeedData,
        current_class_args: CourseClass,
        seed_presencas_args: list[Tuple],
        is_today: bool,
        validate_interval: bool,
        request_time: datetime,
        expected_response: dict,
    ):
        with freeze_time(request_time) as frozen_datetime:
            client_context.app.dependency_overrides[Schedule] = lambda: mocker.Mock(
                get_current_class=lambda: CourseClass(*current_class_args))

        
            for presenca_args in seed_presencas_args:
                seed_presenca(db_context.session, seed_db_data.student.id, *seed_presencas_args)

            # TODO: sem testar date handler (criar novo)
            client_context.app.dependency_overrides[DateHandler] = lambda: mocker.Mock(
                is_today=mocker.Mock(return_value=is_today),
                validate_interval=mocker.Mock(return_value=validate_interval),
            )
    
            response = client_context.client.post(
                f"/presenca/{seed_db_data.student.cpf}", auth=client_context.credentials
            )

        presenca = db_context.session.query(Presenca).order_by(Presenca.id.desc()).first()
        assert response.status_code == expected_response["status_code"]
        assert presenca.student_id == seed_db_data.student.id
        assert presenca.late == expected_response["late"]
        assert presenca.absence == expected_response["absence"]
        assert presenca.created_at == expected_response["created_at"]
        assert presenca.first_half == expected_response["first_half"]
