import os
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.errors.auth_exception import NotAuthorized
from src.services.students_service import StudentService

router = APIRouter(prefix="/presenca")


security = HTTPBasic()
username = os.getenv("ADMIN_USERNAME")
password = os.getenv("ADMIN_PASSWORD")


@router.post("/{cpf_number}", name="Adicionar presença")
def add_attendance(
    cpf_number: str,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    service: StudentService = Depends(StudentService),
):
    if credentials.username != username or credentials.password != password:
        raise NotAuthorized("Usuário ou senha inválidos")

    service.add_attendance(cpf_number)

    return Response(status_code=201)
