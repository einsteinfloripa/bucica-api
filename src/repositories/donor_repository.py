from fastapi import Depends
from src.database.session import get_db
from src.models.students_model import CadastroAlunos
from src.repositories.base_repository import AppRepository

from src.models.donor_model import DonorModel
from src.schemas.donor_schema import DonorSchema

class DonorRepository(AppRepository):
    def __init__(self, db=Depends(get_db)):
        super().__init__(db, CadastroAlunos)

    def add_donor(self, donor: DonorSchema):
        donormodel = DonorModel(name=donor.name, amount=donor.amount, indication=donor.indication)
        self.db.add(donormodel)
        self.db.commit()
        self.db.refresh(donormodel)