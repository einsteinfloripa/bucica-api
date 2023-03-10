from sqlalchemy import Column, DateTime, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StudantItem(Base):
    __tablename__ = "studant_items"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    cpf = Column(String, index=True)
    email = Column(String)
    phone = Column(String)
    attendance = Sequence[Column(DateTime)]
