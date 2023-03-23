from typing import Any, List

from src.database.session import DBSessionMixin


class AppRepository(DBSessionMixin):
    def get_first(self, **kwargs) -> Any | None:
        """
        Get first object from database using the specified kwargs as filters

        The object kwarg is required to specify wich object/table to query
        this kwarg accepts a sqlalchemy mapped class as value

        example: object=User -> will query the User table
        """
        obj = kwargs.pop("object")
        self.db.query(obj).filter_by(**kwargs).first()

    def get(self, **kwargs) -> List[Any] | None:
        """
        Get all objects from database using the specified kwargs as filters

        The object kwarg is required to specify wich object/table to query
        this kwarg accepts a sqlalchemy mapped class as value

        example: object=User -> will query the User table
        """
        obj = kwargs.pop("object")
        self.db.query(obj).filter_by(**kwargs).all()
