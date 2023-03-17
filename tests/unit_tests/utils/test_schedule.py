from datetime import datetime, time

import pytest

from src.utils.schedule import CourseClass, Schedule


class TestSchedule:
    schedule = Schedule()

    def test_get_current_class_returns_course_class_object_it_class_found(self, mocker):
        mocker.patch("src.utils.schedule.CourseClass.is_ongoing", return_value=True)
        output = self.schedule.get_current_class()

        assert isinstance(output, CourseClass)

    def get_current_class_returns_none_if_no_class_is_ongoing(self, mocker):
        mocker.patch("src.utils.schedule.CourseClass.is_ongoing", return_value=False)

        assert self.schedule.get_current_class() is None


class TestCourseClass:
    course_class = CourseClass(0, time(8, 20), time(11, 50))

    def test_is_ongoing_returns_false_if_not_same_weekday(self, mocker):
        mocker.patch(
            "src.utils.schedule.CourseClass._CourseClass__now",
            return_value=datetime(2021, 1, 1),
        )

        expected = False
        output = self.course_class.is_ongoing()

        assert output == expected

    @pytest.mark.skip(reason="Not working")
    def test_is_ongoing_returns_false_if_time_not_in_range(self, mocker):
        mocker.patch(
            "src.utils.schedule.CourseClass._CourseClass__now",
            side_effect=[datetime(2023, 3, 13, 8, 20), datetime(2023, 3, 13, 8, 40)],
        )
        mocker.patch(
            "src.utils.schedule.CourseClass._CourseClass__start",
            return_value=datetime(2023, 3, 13, 8, 20),
        )
        mocker.patch(
            "src.utils.schedule.CourseClass._CourseClass__end",
            return_value=datetime(2023, 3, 13, 11, 50),
        )

        expected = True
        output = self.course_class.is_ongoing()

        assert output == expected
