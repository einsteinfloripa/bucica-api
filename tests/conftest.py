# TODO: Arrumar o erro do mypy sobre importação
import os   


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.base_model import Base
from src.models.students_model import CadastroAlunos

### DATA BASE FIXTURES ###


class DbContext:
    def __init__(self) -> None:
        engine = create_engine(os.getenv("DB_URL"), connect_args={"check_same_thread": False})
        test_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        test_session = test_session_maker()

        self.engine = engine
        self.session = test_session

@pytest.fixture(scope="function")
def session():
    db_context = DbContext()
    yield db_context.session
    db_context.session.close()

def seed_db_data():
    """Seed database with test data."""

    db_context = DbContext()

    db = db_context.session

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

    db.add(student)
    db.commit()
    db.refresh(student)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    db_context = DbContext()

    Base.metadata.drop_all(bind=db_context.engine)
    Base.metadata.create_all(bind=db_context.engine)

    seed_db_data()

    yield

    Base.metadata.drop_all(bind=db_context.engine)


###


### AUTHENTICATION FIXTURES


class ClientContext:
    def __init__(self) -> None:
        self.app = app
        self.client = TestClient(app)
        self.credentials = (os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"))


@pytest.fixture(scope="function")
def client_context():
    """Test client initiation for all tests."""
    yield ClientContext()


###
