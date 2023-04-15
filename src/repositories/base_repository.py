from typing import Any, List


class AppRepository:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def get_first(self, **kwargs) -> Any | None:
        """
        Get first object from database using the specified kwargs as filters

        The object kwarg is required to specify which object/table to query
        this kwarg accepts a sqlalchemy mapped class as value

        example: object=User -> will query the User table
        """
        return self.db.query(self.model).filter_by(**kwargs).first()

    def get_last(self, **kwargs) -> Any | None:
        """
        Get last object from database using the specified kwargs as filters

        The object kwarg is required to specify which object/table to query
        this kwarg accepts a sqlalchemy mapped class as value

        example: object=User -> will query the User table
        """
        return self.db.query(self.model).filter_by(**kwargs).order_by(self.model.id.desc()).first()

    def get(self, **kwargs) -> List[Any] | None:
        """
        Get all objects from database using the specified kwargs as filters

        The object kwarg is required to specify which object/table to query
        this kwarg accepts a sqlalchemy mapped class as value

        example: object=User -> will query the User table
        """
        return self.db.query(self.model).filter_by(**kwargs).all()

    def get_all(self) -> List[Any] | None:
        return self.db.query(self.model).all()
