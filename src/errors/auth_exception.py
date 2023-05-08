from typing import Optional

from .base_exception import AppExceptionBase


class NotAuthorized(AppExceptionBase):
    def __init__(self, message: Optional[str] = ""):
        """
        Not authorized
        """
        status_code = 401
        AppExceptionBase.__init__(self, status_code, message)
