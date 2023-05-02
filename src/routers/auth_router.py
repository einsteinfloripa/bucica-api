import os
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.errors.auth_exception import NotAuthorized

router = APIRouter()


security = HTTPBasic()
username = os.getenv("ADMIN_USERNAME")
password = os.getenv("ADMIN_PASSWORD")


@router.post("/login", name="Fazer Login")
def add_attendance(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    if credentials.username != username or credentials.password != password:
        raise NotAuthorized("Usuário ou senha inválidos")

    return Response(status_code=200)
