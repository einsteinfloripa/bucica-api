from fastapi import APIRouter

from src.services.studants_services import StudantService
from src.utils.service_results import handle_result

router = APIRouter(prefix="/presenca")


@router.post("/{cpf_number}")
def update_attandence(cpf_number: str):
    result = StudantService().create_attendence_check(cpf_number)
    return handle_result(result)


@router.get("/{cpf_number}")
def get_studant(cpf_number: str):
    result = StudantService().get_studant(cpf_number)
    return handle_result(result)
