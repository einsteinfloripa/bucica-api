from datetime import datetime

import pytest
from freezegun import freeze_time

from src.utils.date_handler import DateHandler


class TestDateHandler:
    date_handler_instance = DateHandler()

    @pytest.mark.parametrize(
        "date_time, expected",
        [
            (datetime(2023, 1, 1, 12), True),  # ano novo
            (datetime(2023, 4, 21, 12), True),  # tiradentes
            (datetime(2023, 6, 2, 12), False),
            (datetime(2023, 9, 7, 12), True),  # independencia
            (datetime(2023, 4, 13, 12), False),
        ],
    )
    def test_is_holiday(self, date_time, expected):
        assert self.date_handler_instance.is_holiday(date_time) == expected

    @pytest.mark.parametrize(
        "date, start, end, expected",
        [
            (datetime(2021, 1, 1, 12), datetime(2021, 1, 1, 12), datetime(2021, 1, 1, 13), True),
            (datetime(2021, 1, 1, 12), datetime(2021, 1, 1, 13), datetime(2021, 1, 1, 14), False),
            (datetime(2021, 1, 1, 12), datetime(2021, 1, 1, 11), datetime(2021, 1, 1, 12), True),
            (datetime(2021, 1, 1, 13),datetime(2020, 12, 31, 12),datetime(2020, 12, 31, 14),False)
        ],
    )
    def test_between(self, date, start, end, expected):
        assert self.date_handler_instance.between(date, start, end) == expected

    @pytest.mark.parametrize(
        "mocked_datetime, expected",
        [
            ("2023-01-05", True),
            # edge cases
            ("2023-03-07", True),
            ("2023-03-08", False),
            ("2000-05-04", False),
            # edge cases
            ("2023-12-10", False),
            ("2023-12-11", True),
            ("2023-12-30", True),
        ],
    )
    def test_is_on_vacation_time(self, mocked_datetime, expected):
        with freeze_time(mocked_datetime):
            assert self.date_handler_instance.in_vacation_time() == expected
