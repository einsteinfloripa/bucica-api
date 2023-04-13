import datetime
import time
from unittest import mock

import pytest

from src.models.students_model import Presenca
from src.utils.schedule import CourseClass, LateTypes, Schedule
from tests.conftest import ClientContext, DbContext, SeedData


class TestPresencaCpfNumber:
    """
    TODO: adicionar um app_exception na resosta da solicitaçao abaixo


    def test_not_authenticated_user(self, client_context: ClientContext):
        response = client_context.client.post("/presenca/12345678901")
        print(response.json())
        assert response.status_code == 401
        assert response.json()["app_exception"] == ""
    """

    def test_invalid_user_credentials(self, client_context: ClientContext):
        response = client_context.client.post(
            "/presenca/12345678901", auth=("something", "something")
        )
        assert response.status_code == 401
        assert response.json()["app_exception"] == "NotAuthorized"

    def test_student_not_found_in_data_base(self, client_context: ClientContext):
        response = client_context.client.post(
            "/presenca/12345678901", auth=client_context.credentials
        )
        assert response.status_code == 404
        assert response.json()["app_exception"] == "StudentNotFound"

    @mock.patch(
        "src.utils.schedule.Schedule.get_current_class",
        return_value=None,
    )
    def test_attendace_request_not_on_class_time(
        self, client_context: ClientContext, seed_db_data: SeedData
    ):
        response = client_context.client.post(
            f"/presenca/{seed_db_data.student.cpf}", auth=client_context.credentials
        )
        assert response.status_code == 400
        assert response.json()["app_exception"] == "NotOngoingLesson"

    @mock.patch(
        "src.utils.schedule.Schedule",
        new=mock.MagicMock(get_current_class=lambda: CourseClass(0, time(17, 00), time(19, 00))),
    )
    @pytest.mark.erro
    def test_attendace_successfully_created(
        self,
        client_context: ClientContext,
        seed_db_data: SeedData,
        db_context: DbContext,
    ):
        response = client_context.client.post(
            f"/presenca/{seed_db_data.student.cpf}", auth=client_context.credentials
        )

        new_attendance = (
            db_context.session.query(Presenca)
            .filter(
                Presenca.student_id
                == seed_db_data.student.id
                # Presenca.created_at == datetime.datetime(2023, 3, 13, 18, 0),
            )
            .first()
        )

        assert response.status_code == 201

        assert new_attendance.student_id == seed_db_data.student.id
        # assert new_attendance.created_at == datetime.datetime(2023, 3, 13, 18, 0)
        assert new_attendance.id is not None
        assert new_attendance.first_half is True
        assert new_attendance.absence is False
        assert new_attendance.late == LateTypes.ON_TIME
