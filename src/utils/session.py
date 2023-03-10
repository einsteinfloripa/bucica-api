from datetime import datetime
from typing import List

from src.schemas.studants import StudantSchema


class MockDataBase:
    def __init__(self) -> None:
        self.data: List[StudantSchema] = [
            StudantSchema(
                cpf="00000000000",
                name="Jhon Doe",
                email="johndoe@gmail.com",
                attendence=[datetime.now()],
            )
        ]

    def get(self, key: str) -> StudantSchema | None:
        for item in self.data:
            if item.cpf == key:
                return item
        return None


mockdb = MockDataBase()


class DBSessionMixin:
    def __init__(self, db: MockDataBase = mockdb):
        self.db = db


class AppService(DBSessionMixin):
    pass


class AppRepositorie(DBSessionMixin):
    pass
