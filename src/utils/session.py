from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DBSessionMixin:
    def __init__(self, db: Session = SessionLocal()):
        self.db = db
