from pydantic import BaseModel


class StudantSchema(BaseModel):
    name: str = ""
    cpf: str = ""
    email: str = ""
    phone: str = ""

    class Config:
        orm_mode = True
