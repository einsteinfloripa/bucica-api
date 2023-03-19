from fastapi import APIRouter, Response

from src.services.students_service import StudentService

router = APIRouter(prefix="/presenca")


service = StudentService()


@router.post("/{cpf_number}", name="Adicionar presença")
def add_attendance(cpf_number: str):
    service.add_attendance(cpf_number)

    return Response(status_code=201)
