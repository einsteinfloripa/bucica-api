from fastapi import FastAPI

from src.routers import check_attandance
from src.utils.app_exceptions import AppExceptionCase, app_exception_handler

app = FastAPI()


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, exc):
    return await app_exception_handler(request, exc)


app.include_router(check_attandance.router)
