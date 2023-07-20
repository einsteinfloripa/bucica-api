from datetime import datetime, date

import pytest
from freezegun import freeze_time

from src.utils.date_handler import DateHandler

class TestDateHandler:
    @freeze_time("2021-01-01 12:00:00")
    def test_is_today(self):
        date_dadler_instance = DateHandler()
        today = datetime.now()
        assert date_dadler_instance.is_today(today)

    @pytest.mark.parametrize("date_time, expected", [
        (datetime(2023, 1, 1, 12), True), # ano novo
        (datetime(2023, 4, 21, 12), True), # tiradentes
        (datetime(2023, 6, 2, 12), False),
        (datetime(2023, 9, 7, 12), True), # independencia
        (datetime(2023, 4, 13, 12), False),
    ])
    def test_is_holiday(self, date_time, expected):
        date_dadler_instance = DateHandler()
        assert date_dadler_instance.is_holiday(date_time) == expected


