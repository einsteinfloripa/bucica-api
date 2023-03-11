from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./bucica.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DBSessionMixin:
    def __init__(self, db: Session = SessionLocal()):
        self.db = db


class AppService(DBSessionMixin):
    pass


class AppRepositorie(DBSessionMixin):
    pass
