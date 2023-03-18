from fastapi import Request
from fastapi.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict = None) -> None:
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self) -> str:
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


class AppException:
    class StudantUpdateAttendance(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Update failed
            """
            status_code = 500  # FIXME what status code ???
            AppExceptionCase.__init__(self, status_code, context)

    class StudentNotFound(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Stutand not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class StudantItemRequiresAuth(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item is not public and requires auth
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)

    class OngoingClassNotFound(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Class not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class AttendanceAlreadyConfirmed(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Class not found
            """
            status_code = 400
            AppExceptionCase.__init__(self, status_code, context)


def app_exception_handler(request: Request, exc: AppExceptionCase) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )
