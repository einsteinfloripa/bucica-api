import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DBSessionMixin:
    def __init__(self, db: Session = init_db()):
        self.db = db
