from fastapi import APIRouter

from schemas.attendence_schemas import AttendanceCheckSuccess, Cpf
from src.services.studants import StudantService
from src.utils.service_results import handle_result
from src.utils.session import MockDataBase

router = APIRouter(prefix="/presença/")


@router.post("/{cpf_number}/", response_model=AttendanceCheckSuccess)
async def update_attandence(item: Cpf, db: MockDataBase):
    result = StudantService(db).update_attendence(item)
    return handle_result(result)
