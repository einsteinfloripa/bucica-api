import datetime
from typing import Literal
from unittest import mock

import pytest

from src.utils.schedule import (
    CourseClass,
    FirstClassHalf,
    LateTypes,
    Schedule,
    SecondClassHalf,
    Weekday,
)


class TestCourseClass:
    @pytest.mark.parametrize(
        "start, end, expected",
        [
            (FirstClassHalf.BEGIN.value, FirstClassHalf.END.value, True),
            (SecondClassHalf.BEGIN.value, SecondClassHalf.END.value, False),
        ],
    )
    @mock.patch(
        "src.utils.schedule.datetime",
        new=mock.MagicMock(
            combine=datetime.datetime.combine,
            today=lambda: datetime.datetime(2023, 3, 13, 17, 55),
            now=lambda: datetime.datetime(2023, 3, 13, 17, 55),
        ),
    )
    def test_is_ongoing(self, start: datetime.time, end: datetime.time, expected: bool):
        course_class = CourseClass(Weekday.MONDAY.value, start, end)

        assert course_class.is_ongoing() == expected

    @pytest.mark.parametrize(
        "mocked_time, start, end, expected",
        [
            (
                datetime.datetime(2023, 3, 13, 17, 50),
                FirstClassHalf.BEGIN.value,
                FirstClassHalf.END.value,
                LateTypes.ON_TIME,
            ),
            (
                datetime.datetime(2023, 3, 13, 18, 15),
                FirstClassHalf.BEGIN.value,
                FirstClassHalf.END.value,
                LateTypes.ON_TIME,
            ),
            (
                datetime.datetime(2023, 3, 13, 18, 16),
                FirstClassHalf.BEGIN.value,
                FirstClassHalf.END.value,
                LateTypes.HALF_LATE,
            ),
            (
                datetime.datetime(2023, 3, 13, 18, 50),
                FirstClassHalf.BEGIN.value,
                FirstClassHalf.END.value,
                LateTypes.HALF_LATE,
            ),
            (
                datetime.datetime(2023, 3, 13, 18, 51),
                FirstClassHalf.BEGIN.value,
                FirstClassHalf.END.value,
                LateTypes.LATE,
            ),
            (
                datetime.datetime(2023, 3, 13, 20, 20),
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
                LateTypes.ON_TIME,
            ),
            (
                datetime.datetime(2023, 3, 13, 20, 45),
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
                LateTypes.ON_TIME,
            ),
            (
                datetime.datetime(2023, 3, 13, 20, 46),
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
                LateTypes.HALF_LATE,
            ),
            (
                datetime.datetime(2023, 3, 13, 21, 20),
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
                LateTypes.HALF_LATE,
            ),
            (
                datetime.datetime(2023, 3, 13, 21, 21),
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
                LateTypes.LATE,
            ),
        ],
    )
    def test_is_late(
        self,
        mocked_time: datetime.datetime,
        start: datetime.time,
        end: datetime.time,
        expected: Literal[LateTypes.ON_TIME, LateTypes.HALF_LATE, LateTypes.LATE],
    ):
        with mock.patch(
            "src.utils.schedule.datetime",
            new=mock.MagicMock(
                today=lambda: mocked_time,
                now=lambda: mocked_time,
                timedelta=datetime.timedelta,
                combine=datetime.datetime.combine,
            ),
        ):
            course_class = CourseClass(Weekday.MONDAY.value, start, end)
            assert course_class.is_late() == expected

    @pytest.mark.parametrize(
        "mocked_function_return, expected",
        [
            (True, False),
            (False, True),
        ],
    )
    def test_is_absent(self, mocked_function_return: bool, expected: bool):
        with mock.patch(
            "src.utils.schedule.CourseClass.is_ongoing", return_value=mocked_function_return
        ):
            course_class = CourseClass(
                Weekday.MONDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value
            )
            assert course_class.is_absent() == expected


class TestSchedule:
    schedule = Schedule()

    def test_get_current_class_when_is_ongoing_is_none(self):
        with mock.patch(
            "src.utils.schedule.CourseClass.is_ongoing",
            return_value=False,
        ):
            current_class = self.schedule.get_current_class()
            assert current_class is None

    @pytest.mark.parametrize(
        "mocked_function_return, weekday, start, end",
        [
            ([True], Weekday.MONDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value),
            (
                [False, True],
                Weekday.MONDAY.value,
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
            ),
            (
                [False, False, True],
                Weekday.TUESDAY.value,
                FirstClassHalf.BEGIN.value,
                FirstClassHalf.END.value,
            ),
            (
                [False, False, False, True],
                Weekday.TUESDAY.value,
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
            ),
            (
                [False, False, False, False, True],
                Weekday.WEDNESDAY.value,
                FirstClassHalf.BEGIN.value,
                FirstClassHalf.END.value,
            ),
            (
                [False, False, False, False, False, True],
                Weekday.WEDNESDAY.value,
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
            ),
            (
                [False, False, False, False, False, False, True],
                Weekday.THURSDAY.value,
                FirstClassHalf.BEGIN.value,
                FirstClassHalf.END.value,
            ),
            (
                [False, False, False, False, False, False, False, True],
                Weekday.THURSDAY.value,
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
            ),
            (
                [False, False, False, False, False, False, False, False, True],
                Weekday.FRIDAY.value,
                FirstClassHalf.BEGIN.value,
                FirstClassHalf.END.value,
            ),
            (
                [False, False, False, False, False, False, False, False, False, True],
                Weekday.FRIDAY.value,
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
            ),
        ],
    )
    def test_get_current_class_with_mocked_values(
        self, mocked_function_return, start, end, weekday
    ):
        with mock.patch(
            "src.utils.schedule.CourseClass.is_ongoing", side_effect=mocked_function_return
        ):
            current_class = self.schedule.get_current_class()
            assert current_class.weekday == weekday
            assert current_class.start.time() == start
            assert current_class.end.time() == end
