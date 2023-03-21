from typing import Any, List

from src.database.session import DBSessionMixin


class AppRepository(DBSessionMixin):
    def get_first(self, **kwargs) -> Any:
        obj = kwargs.pop("object")
        self.db.query(obj).filter_by(**kwargs).first()

    def get(self, **kwargs) -> List[Any]:
        obj = kwargs.pop("object")
        self.db.query(obj).filter_by(**kwargs).all()
