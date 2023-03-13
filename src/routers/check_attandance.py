from typing import Any

from fastapi import APIRouter

from src.services.studants import StudantService
from src.utils.service_results import handle_result

router = APIRouter(prefix="/presenca")


@router.post("/{cpf_number}")
async def update_attandence(cpf_number: str):
    result = StudantService().update_attendence(cpf_number)
    return handle_result(result)


@router.get("/{cpf_number}")
async def get_studant(cpf_number: str):
    result = StudantService().get_studant(cpf_number)
    return handle_result(result)
