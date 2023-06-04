import pytest
from faker import Faker
from pytest_mock import MockerFixture
from src.errors.students_exception import (
    AttendanceAlreadyConfirmed,
    NotOngoingClass,
    StudentNotFound,
)

from src.models.students_model import CadastroAlunos, Presenca
from src.services.students_service import StudentService
from src.utils.schedule import CourseClass, FirstClassHalf, LateTypes, SecondClassHalf

fake = Faker()


@pytest.mark.unit
class TestStudentService:
    @pytest.fixture
    def course_class_data(self):
        course_class = CourseClass(
            weekday=1,
            start_time=FirstClassHalf.BEGIN.value,
            end_time=FirstClassHalf.END.value,
        )
        course_class.id = 1
        return course_class

    @pytest.fixture
    def student_data(self):
        aluno = CadastroAlunos(
            name=fake.name(),
            cpf="12345678900",
            email=fake.email(),
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

    @pytest.fixture
    def attendance_data(self):
        presenca = Presenca(
            student_id=1,
            absence=False,
            late=LateTypes.ON_TIME,
            first_half=True,
        )

        presenca.id = 1
        return presenca

    @pytest.fixture
    def mock_schedule(self):
        pass

    @pytest.fixture
    def mock_student_repository(self):
        pass

    @pytest.fixture
    def mock_attendance_repository(self):
        pass

    @pytest.fixture
    def mock_date_handler(self):
        pass

    def test_student_not_found(self, mocker: MockerFixture):
        mock_student_repository = mocker.Mock(get_by_cpf=mocker.Mock(return_value=None))

        service = StudentService(
            student_repository=mock_student_repository,
            attendance_repository=mocker.Mock(),
            schedule=mocker.Mock(),
            date_handler=mocker.Mock(),
        )

        with pytest.raises(StudentNotFound) as app_exception:
            service.add_attendance("12345678900")

        assert app_exception.type.__name__ == "StudentNotFound"
        assert app_exception.value.message == "CPF do Aluno não encontrado"
        assert app_exception.value.status_code == 404

    def test_ongoing_class_not_found(self, mocker: MockerFixture, student_data):
        mock_student_repository = mocker.Mock(get_by_cpf=mocker.Mock(return_value=student_data))
        mock_schedule = mocker.Mock(get_current_class=mocker.Mock(return_value=None))
        service = StudentService(
            student_repository=mock_student_repository,
            attendance_repository=mocker.Mock(),
            schedule=mock_schedule,
            date_handler=mocker.Mock(),
        )

        with pytest.raises(NotOngoingClass) as app_exception:
            service.add_attendance("12345678900")

        assert app_exception.type.__name__ == "NotOngoingClass"
        assert (
            app_exception.value.message
            == f"Não há aula em andamento. As presenças só podem ser registradas nos intervalo entre {FirstClassHalf.begin_time_str()} até {FirstClassHalf.end_time_str()} e {SecondClassHalf.begin_time_str()} até {SecondClassHalf.end_time_str()}"
        )
        assert app_exception.value.status_code == 400

    def test_attendance_already_confirmed(
        self, mocker: MockerFixture, student_data, course_class_data, attendance_data
    ):
        mock_student_repository = mocker.Mock(get_by_cpf=mocker.Mock(return_value=student_data))
        mock_schedule = mocker.Mock(get_current_class=mocker.Mock(return_value=course_class_data))
        mock_attendance_repository = mocker.Mock(
            get_last_with=mocker.Mock(return_value=attendance_data)
        )
        mock_date_handler = mocker.Mock(
            is_today=mocker.Mock(return_value=True),
            validate_interval=mocker.Mock(return_value=True),
        )

        service = StudentService(
            student_repository=mock_student_repository,
            attendance_repository=mock_attendance_repository,
            schedule=mock_schedule,
            date_handler=mock_date_handler,
        )

        with pytest.raises(AttendanceAlreadyConfirmed) as app_exception:
            service.add_attendance("12345678900")
        assert app_exception.type.__name__ == "AttendanceAlreadyConfirmed"
        assert app_exception.value.message == "Presença já confirmada"
        assert app_exception.value.status_code == 400

    def test_add_attendance(
        self,
        mocker: MockerFixture,
        student_data,
        course_class_data,
        attendance_data,
    ):
        mock_student_repository = mocker.Mock(get_by_cpf=mocker.Mock(return_value=student_data))
        mock_schedule = mocker.Mock(get_current_class=mocker.Mock(return_value=course_class_data))
        mock_attendance_repository = mocker.Mock(
            get_last_with=mocker.Mock(return_value=attendance_data)
        )
        mock_date_handler = mocker.Mock(
            is_today=mocker.Mock(return_value=False),
            validate_interval=mocker.Mock(return_value=False),
        )

        service = StudentService(
            student_repository=mock_student_repository,
            attendance_repository=mock_attendance_repository,
            schedule=mock_schedule,
            date_handler=mock_date_handler,
        )
        service.add_attendance("12345678900")

        assert mock_student_repository.get_by_cpf.call_count == 1
        assert mock_attendance_repository.get_last_with.call_count == 1
        assert mock_schedule.get_current_class.call_count == 1
        assert mock_date_handler.is_today.call_count == 1
        assert mock_date_handler.validate_interval.call_count == 1
        assert mock_attendance_repository.create_attendance.call_count == 1
