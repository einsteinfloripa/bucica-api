import datetime
from unittest import mock

import pytest
from faker import Faker

from src.models.students_model import CadastroAlunos, Presenca
from src.services.students_service import StudentService
from src.utils.schedule import LateTypes

fake = Faker()


def student_data():
    aluno = CadastroAlunos(
        name=fake.name(),
        cpf="12345678900",
        email=fake.email(),
        birthdate=fake.date_of_birth(),
        cep=fake.postcode(),
        city=fake.city(),
        state=fake.state(),
        street=fake.street_name(),
        number=fake.phone_number(),
        civil_state=fake.random_element(elements=("Solteiro", "Casado")),
        complement=fake.random_element(elements=("Casa", "Apartamento")),
        neighborhood=fake.random_element(elements=("Centro", "Bairro")),
        phone=fake.phone_number(),
        rg=fake.random_element(elements=("12345678900", "12345678901")),
    )

    aluno.id = 1
    return aluno


def attendance_data():
    presenca = Presenca(
        student_id=1,
        absence=False,
        late=LateTypes.ON_TIME,
    )

    presenca.id = 1
    return presenca


class TestStudentService:
    @mock.patch("src.services.students_service.StudentRepository.get_by_cpf", return_value=None)
    def test_student_not_found(self, mock_get_by_cpf):
        service = StudentService()
        with pytest.raises(Exception) as app_exception:
            service.add_attendance("12345678900")

        assert app_exception.type.__name__ == "StudentNotFound"
        assert app_exception.value.message == "CPF do Aluno não encontrado"
        assert app_exception.value.status_code == 404

    @mock.patch(
        "src.services.students_service.StudentRepository.get_by_cpf",
        return_value=student_data(),
    )
    @mock.patch("src.services.students_service.Schedule.get_current_class", return_value=None)
    def test_ongoing_class_not_found(self, mock_get_by_cpf, mock_get_current_class):
        service = StudentService()

        with pytest.raises(Exception) as app_exception:
            service.add_attendance("12345678900")

        assert app_exception.type.__name__ == "NotOngoingLesson"
        assert app_exception.value.message == "Não há aula em andamento"
        assert app_exception.value.status_code == 400

    @mock.patch(
        "src.services.students_service.StudentRepository.get_by_cpf",
        return_value=student_data(),
    )
    @mock.patch("src.services.students_service.Schedule.get_current_class", return_value="class")
    @mock.patch(
        "src.services.students_service.AttendanceRepository.get_attendance_by_student_id",
        return_value=attendance_data(),
    )
    def test_attendance_already_confirmed(
        self, mock_get_by_cpf, mock_get_current_class, mock_get_attendance_by_student_id
    ):
        service = StudentService()

        with pytest.raises(Exception) as app_exception:
            service.add_attendance("12345678900")
        assert app_exception.type.__name__ == "AttendanceAlreadyConfirmed"
        assert app_exception.value.message == "Presença já confirmada"
        assert app_exception.value.status_code == 400

    @mock.patch(
        "src.services.students_service.StudentRepository.get_by_cpf",
        return_value=student_data(),
    )
    @mock.patch("src.services.students_service.Schedule.get_current_class", return_value="class")
    @mock.patch(
        "src.services.students_service.AttendanceRepository.get_attendance_by_student_id",
        return_value=None,
    )
    @mock.patch(
        "src.services.students_service.AttendanceRepository.create_attendance",
        return_value=None,
    )
    def test_add_attendance(
        self,
        mock_get_by_cpf,
        mock_get_current_class,
        mock_get_attendance_by_student_id,
        mock_create_attendance,
    ):
        service = StudentService()
        service.add_attendance("12345678900")

        assert mock_get_by_cpf.called
        assert mock_get_current_class.called
        assert mock_get_attendance_by_student_id.called
        assert mock_create_attendance.called
