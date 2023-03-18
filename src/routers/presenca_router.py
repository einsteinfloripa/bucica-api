from fastapi import APIRouter

from src.services.students_service import StudentService
from src.utils.service_results import handle_result

router = APIRouter(prefix="/presenca")


service = StudentService()


@router.post("/{cpf_number}")
def update_attendance(cpf_number: str):
    result = service.add_attendance(cpf_number)
    return handle_result(result)


@router.get("/{cpf_number}")
def get_student(cpf_number: str):
    result = service.get_student(cpf_number)
    return handle_result(result)
