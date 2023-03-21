from datetime import date, datetime
from typing import TypedDict

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.utils.schedule import LateTypes


class CadastroAlunos(Base):
    __tablename__ = "Cadastro_Alunos"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(name="nome")
    phone: Mapped[str] = mapped_column(name="telefone")
    birthdate: Mapped[date] = mapped_column(name="data_nascimento")
    rg: Mapped[str] = mapped_column(name="rg")
    cpf: Mapped[str] = mapped_column(name="cpf", unique=True)
    civil_state: Mapped[str] = mapped_column(name="estado_civil")
    state: Mapped[str] = mapped_column(name="estado")
    city: Mapped[str] = mapped_column(name="cidade")
    neighborhood: Mapped[str] = mapped_column(name="bairro")
    street: Mapped[str] = mapped_column(name="rua")
    number: Mapped[str] = mapped_column(name="numero")
    complement: Mapped[str] = mapped_column(name="complemento")
    cep: Mapped[str] = mapped_column(name="cep")
    email: Mapped[str] = mapped_column(name="email")

    presencas = relationship("Presenca", back_populates="students")

    def __init__(
        self,
        name: str,
        phone: str,
        birthdate: date,
        rg: str,
        cpf: str,
        civil_state: str,
        state: str,
        city: str,
        neighborhood: str,
        street: str,
        number: str,
        complement: str,
        cep: str,
        email: str,
    ):
        self.name = name
        self.phone = phone
        self.birthdate = birthdate
        self.rg = rg
        self.cpf = cpf
        self.civil_state = civil_state
        self.state = state
        self.city = city
        self.neighborhood = neighborhood
        self.street = street
        self.number = number
        self.complement = complement
        self.cep = cep
        self.email = email

    def __repr__(self):
        return f"CadastroAlunos(id={self.id}, name={self.name}, phone={self.phone}, birthdate={self.birthdate}, rg={self.rg}, cpf={self.cpf}, civil_state={self.civil_state}, state={self.state}, city={self.city}, neighborhood={self.neighborhood}, street={self.street}, number={self.number}, complement={self.complement}, cep={self.cep}, email={self.email})"


class Presenca(Base):
    __tablename__ = "Presenca"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("Cadastro_Alunos.id"), name="aluno_id")
    late: Mapped[LateTypes] = mapped_column(name="atraso")
    absence: Mapped[bool] = mapped_column(name="falta")
    created_at: Mapped[datetime] = mapped_column(name="criado_em", default=datetime.now())
    first_half: Mapped[bool] = mapped_column(name="primeira_metade")

    students = relationship("CadastroAlunos", back_populates="presencas")

    def __init__(
        self,
        student_id: int,
        late: LateTypes,
        absence: bool,
        first_half: bool,
        created_at: datetime = datetime.now(),
    ):
        self.student_id = student_id
        self.late = late
        self.absence = absence
        self.created_at = created_at
        self.first_half = first_half

    def __repr__(self):
        return f"Presenca(id={self.id}, student_id={self.student_id}, late={self.late}, absence={self.absence}, created_at={self.created_at}, first_half={self.first_half})"


class CadastroAlunosTypedDict(TypedDict):
    id: int
    name: str
    phone: str
    birthdate: datetime
    rg: str
    cpf: str
    civil_state: str
    state: str
    city: str
    neighborhood: str
    street: str
    number: str
    complement: str
    cep: str
    email: str
