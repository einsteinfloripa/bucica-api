from datetime import datetime, time

import pytest
from freezegun import freeze_time

from src.utils.date_handler import DateHandler

@freeze_time("2021-01-01 12:00:00")
class TestDateHandler:
    def test_is_today(self):
        date_dadler_instance = DateHandler()
        today = datetime.now()
        assert date_dadler_instance.is_today(today)

    @pytest.mark.parametrize("time, start, end, expected", [
        (time(12, 0, 0), time(10, 0, 0), time(14, 0, 0), True),
        (time(8, 0, 0), time(10, 0, 0), time(14, 0, 0), False),
        (time(16, 0, 0), time(10, 0, 0), time(14, 0, 0), False),
        (time(10, 0, 0), time(10, 0, 0), time(14, 0, 0), True),
        (time(14, 0, 0), time(10, 0, 0), time(14, 0, 0), True),
    ])
    def test_validate_interval(self, time, start, end, expected):
        date_dadler_instance = DateHandler()
        assert date_dadler_instance.validate_interval(time, start, end) == expected