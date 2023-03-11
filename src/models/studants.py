from sqlalchemy import Column, DateTime, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StudantItem(Base):
    __tablename__ = "studant_items"
    name = Column("name", String, index=True)
    cpf = Column("cpf", String, index=True, primary_key=True)
    email = Column("email", String)
    phone = Column("phone", String)

    def __init__(self, name: str, cpf: str, email: str, phone: str) -> None:
        self.name = name
        self.cpf = cpf
        self.email = email
        self.phone = phone

    def __repr__(self) -> str:
        return f"<StudantItem(name='{self.name}', cpf='{self.cpf}', email='{self.email}', phone='{self.phone}')>"
