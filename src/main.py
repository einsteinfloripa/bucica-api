from fastapi import FastAPI

from src.routers.presenca_router import router as CheckAttendanceRouter
from src.utils.app_exceptions import AppExceptionCase, app_exception_handler

app = FastAPI()


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, exc):
    return app_exception_handler(request, exc)


app.include_router(CheckAttendanceRouter)
