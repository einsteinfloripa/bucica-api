from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.errors.base_exception import AppExceptionBase
from src.routers.students_router import router as PresencaRouter

app = FastAPI()


@app.exception_handler(AppExceptionBase)
async def app_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "message": exc.message,
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(PresencaRouter)
