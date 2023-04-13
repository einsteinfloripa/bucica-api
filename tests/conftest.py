# TODO: Arrumar o erro do mypy sobre importação
import os

from datetime import datetime
from typing import Type

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.base_model import Base
from src.models.students_model import CadastroAlunos, Presenca
from src.utils.schedule import LateTypes

### DATA BASE FIXTURES ###


class DbContext:
    def __init__(self, _engine, _session) -> None:
        self.engine = _engine
        self.session = _session


@pytest.fixture(scope="session")
def db_context() -> Type[DbContext]:  # TODO: Arrumar o erro do mypy
    engine = create_engine(os.getenv("DB_URL"), connect_args={"check_same_thread": False})
    test_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    test_session = test_session_maker()  # TODO: Arrumar o erro do mypy
    return DbContext(engine, test_session)


@pytest.fixture(scope="session", autouse=True)
def reset_db(db_context):
    """Redirect request to use testing DB."""
    Base.metadata.drop_all(bind=db_context.engine)
    Base.metadata.create_all(bind=db_context.engine)


class SeedData:
    def __init__(self, student: CadastroAlunos, attendances: list[Presenca]):
        self.student = student
        self.attendances = attendances


@pytest.fixture(scope="function")
def seed_db_data(db_context: DbContext):
    """Seed database with test data."""
    student = CadastroAlunos(
        name="El Dog Bucica",
        cpf="11122233344",
        rg="123456789",
        cep="12345678",
        email="el_dog_bucica@einsteinfloripa.com.br",
        phone="123456789",
        civil_state="Solteiro",
        state="Santa Catarina",
        city="Florianópolis",
        neighborhood="Centro",
        street="Rua 1",
        number="1",
        complement="",
    )

    attendances = [
        Presenca(
            student_id=1,
            late=LateTypes.ON_TIME,
            absence=False,
            first_half=True,
            created_at=datetime(2023, 4, 3, 18, 0, 0),
        ),
        Presenca(
            student_id=1,
            late=LateTypes.HALF_LATE,
            absence=False,
            first_half=True,
            created_at=datetime(2023, 4, 4, 18, 40, 0),
        ),
        Presenca(
            student_id=1,
            late=LateTypes.ON_TIME,
            absence=False,
            first_half=True,
            created_at=datetime(2023, 4, 5, 19, 0, 0),
        ),
    ]

    db_context.session.add(student)
    db_context.session.add_all(attendances)
    db_context.session.commit()

    yield SeedData(student, attendances)

    db_context.session.delete(student)

    for attendance in attendances:
        db_context.session.delete(attendance)

    db_context.session.commit()


###


### AUTHENTICATION FIXTURES


class ClientContext:
    def __init__(self) -> None:
        self.app = app
        self.client = TestClient(app)
        self.credentials = (os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"))


@pytest.fixture(scope="function")
def client_context() -> ClientContext:
    """Test client initiation for all tests."""
    return ClientContext()


###
