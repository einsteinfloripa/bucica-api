from typing import Optional

from .base_exception import AppExceptionBase


class StudentNotFound(AppExceptionBase):
    def __init__(self, message: Optional[str] = ""):
        """
        Stutand not found
        """
        status_code = 404
        AppExceptionBase.__init__(self, status_code, message)


class NotOngoingLesson(AppExceptionBase):
    def __init__(self, message: Optional[str] = ""):
        """
        Not ongoing lesson
        """
        status_code = 400
        AppExceptionBase.__init__(self, status_code, message)


class AttendanceAlreadyConfirmed(AppExceptionBase):
    def __init__(self, message: Optional[str] = ""):
        """
        Attendance already confirmed
        """
        status_code = 400
        AppExceptionBase.__init__(self, status_code, message)
