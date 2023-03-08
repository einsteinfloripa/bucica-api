from typing import Any


class MockDataBase:
    def __init__(self) -> None:
        self.data: Any = {}

    def get(self, key: Any) -> Any:
        return self.data.get(key)

    def set(self, key: Any, value: Any) -> None:
        self.data[key] = value

    def delete(self, key: Any) -> None:
        del self.data[key]

    def clear(self) -> None:
        self.data = {}


mockdb = MockDataBase()


class DBSessionMixin:
    def __init__(self, db: MockDataBase = mockdb):
        self.db = db


class AppService(DBSessionMixin):
    pass


class AppRepositorie(DBSessionMixin):
    pass
