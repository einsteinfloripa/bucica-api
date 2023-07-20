import os
from typing import Annotated
from src.database.session import get_db

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.schemas.donor_schema import DonorSchema
from src.repositories.donor_repository import DonorRepository

router = APIRouter()


@router.post("/donors", name="Donors")
def add_donor(donor: DonorSchema, repository: DonorRepository = Depends(DonorRepository)):

    repository.add_donor(donor)
    
    return Response(status_code=201)