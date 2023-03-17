from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from src.models.base_models import Base
from src.utils.schedule import CourseClass


class CadastroAlunos(Base):
    __tablename__ = "Cadastro_Alunos"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, index=True)
    phone = mapped_column(String)
    birthdate = mapped_column(Date)
    rg = mapped_column(String, unique=True)
    cpf = mapped_column(String, index=True, unique=True)
    civil_state = mapped_column(String)
    state = mapped_column(String)
    city = mapped_column(String)
    neighborhood = mapped_column(String)
    street = mapped_column(String)
    number = mapped_column(String)
    complement = mapped_column(String)
    cep = mapped_column(String)
    email = mapped_column(String)

    presencas = relationship("Presenca", back_populates="studants")


class Presenca(Base):
    __tablename__ = "Presenca"

    id = mapped_column(Integer, primary_key=True)
    studant_id = mapped_column(Integer, ForeignKey("Cadastro_Alunos.id"))
    datetime_of_creation = mapped_column(DateTime)
    late = mapped_column(Enum(CourseClass.Late))
    absence = mapped_column(Boolean)

    studants = relationship("CadastroAlunos", back_populates="presencas")
