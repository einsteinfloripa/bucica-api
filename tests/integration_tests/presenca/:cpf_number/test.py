import datetime
from unittest import mock

import pytest

from tests.conftest import ClientContext


@pytest.mark.usefixtures("seed_db")
class TestPresencaCpfNumber:
    """
    TODO: adicionar um app_exception na resosta da solicitaçao abaixo


    def test_not_authenticated_user(self, client_context: ClientContext):
        resposnse = client_context.client.post("/presenca/12345678901")
        print(resposnse.json())
        assert resposnse.status_code == 401
        assert resposnse.json()["app_exception"] == ""
    """

    def test_invalid_user_credentials(self, client_context: ClientContext):
        resposnse = client_context.client.post(
            "/presenca/12345678901", auth=("something", "something")
        )
        assert resposnse.status_code == 401
        assert resposnse.json()["app_exception"] == "NotAuthorized"

    def test_student_not_found_in_data_base(self, client_context: ClientContext):
        resposnse = client_context.client.post(
            "/presenca/12345678901", auth=client_context.credentials
        )
        assert resposnse.status_code == 404
        assert resposnse.json()["app_exception"] == "StudentNotFound"

    def test_student_not_found_in_data_base(self, client_context: ClientContext):
        resposnse = client_context.client.post(
            "/presenca/12345678901", auth=client_context.credentials
        )
        assert resposnse.status_code == 404
        assert resposnse.json()["app_exception"] == "StudentNotFound"

    @mock.patch(
        "src.utils.schedule.datetime",
        new=mock.MagicMock(
            today=lambda: datetime.datetime(2023, 3, 13, 16, 0),
            now=lambda: datetime.datetime(2023, 3, 13, 16, 0),
        ),
    )
    def test_attendace_request_not_on_class_time(self, client_context: ClientContext):
        resposnse = client_context.client.post(
            "/presenca/11122233344", auth=client_context.credentials
        )
        assert resposnse.status_code == 404
        assert resposnse.json()["app_exception"] == "NotOngoingClass"

    @pytest.mark.usefixtures("seed_db")
    def test_attendace_successfully_created(self):
        pass
