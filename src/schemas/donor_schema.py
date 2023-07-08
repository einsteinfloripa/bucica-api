from pydantic import BaseModel, Field


class DonorSchema(BaseModel):
    name: str = Field(..., min_length=3, alias="nome")
    indication: str = Field(..., min_length=3, alias="indicacao")
    amount: float = Field(..., alias="quantidade")