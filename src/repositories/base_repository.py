from typing import Any, List

from fastapi import Depends

from src.database.session import get_db


class AppRepository:
    def __init__(self, db=Depends(get_db)):
        self.db = db

    def get_first(self, **kwargs) -> Any | None:
        """
        Get first object from database using the specified kwargs as filters

        The object kwarg is required to specify which object/table to query
        this kwarg accepts a sqlalchemy mapped class as value

        example: object=User -> will query the User table
        """
        obj = kwargs.pop("object")
        return self.db.query(obj).filter_by(**kwargs).first()
    
    def get_last(self, **kwargs) -> Any | None:
        """
        Get last object from database using the specified kwargs as filters

        The object kwarg is required to specify which object/table to query
        this kwarg accepts a sqlalchemy mapped class as value

        example: object=User -> will query the User table
        """
        obj = kwargs.pop("object")
        return self.db.query(obj).filter_by(**kwargs).order_by(obj.id.desc()).first()

    def get(self, **kwargs) -> List[Any] | None:
        """
        Get all objects from database using the specified kwargs as filters

        The object kwarg is required to specify which object/table to query
        this kwarg accepts a sqlalchemy mapped class as value

        example: object=User -> will query the User table
        """
        obj = kwargs.pop("object")
        return self.db.query(obj).filter_by(**kwargs).all()
