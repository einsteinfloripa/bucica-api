from typing import Any

from src.utils.app_exceptions import AppExceptionCase


class ServiceResult:
    def __init__(self, arg: Any) -> None:
        if isinstance(arg, AppExceptionCase):
            self.success = False
            self.exception_case = arg.exception_case
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None
        self.value = arg

    def __str__(self) -> str:
        if self.success:
            return "[Success]"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self) -> str:
        if self.success:
            return "<ServiceResult Success>"
        return f"<ServiceResult AppException {self.exception_case}>"

    def __enter__(self):
        return self.value

    def __exit__(self, *kwargs) -> None:
        pass


def handle_result(result: ServiceResult) -> ServiceResult:
    if not result.success:
        with result as exception:
            raise exception
    with result as result:
        return result
