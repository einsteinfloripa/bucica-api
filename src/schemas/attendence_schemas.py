from datetime import datetime

from pydantic import BaseModel

### REQUEST VALUE SCHEMAS ###


class Cpf(BaseModel):
    number: str = ""


### RESPONSE VALUE SCHEMAS ###


class AttendanceCheckSuccess(BaseModel):
    message: str = "Presença anotada com sucesso"
    date: datetime = datetime.now()
