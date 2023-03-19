from typing import Optional


class AppExceptionBase(Exception):
    def __init__(self, status_code: int, message: Optional[str] = "") -> None:
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - message={self.message}>"
        )
