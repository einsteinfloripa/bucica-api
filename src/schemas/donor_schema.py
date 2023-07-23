from pydantic import BaseModel, Field


class DonorSchema(BaseModel):
    name: str = Field(..., alias="nome")
    indication: str = Field(..., alias="indicacao")
    amount: float = Field(..., gt=0, alias="quantidade")