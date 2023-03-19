import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.models.base_model import Base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL", "")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DBSessionMixin:
    def __init__(self, db: Session = SessionLocal()):
        self.db = db
