from datetime import datetime
from typing import List

from pydantic import BaseModel


class StudantSchema(BaseModel):
    name: str = ""
    cpf: str = ""
    email: str = ""
    phone: str = ""
    attendance: List[datetime] = []
