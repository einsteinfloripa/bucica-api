import enum
from datetime import datetime, time


class CourseClass:
    class Late(enum.Enum):
        on_time = 0
        half_late = 1
        late = 2

    def __init__(self, weakday: int, start: time, end: time):
        self.start = datetime.combine(datetime.today(), start)
        self.end = datetime.combine(datetime.today(), end)
        self.lenth = self.end - self.start
        self.weekday = weakday

    def is_ongoing(self) -> bool:
        current_time = datetime.now()
        return self.start <= current_time <= self.end

    def is_late(self) -> Late:
        percentage_of_class_passed = (
            self.start - datetime.now()
        ).total_seconds() / self.lenth.total_seconds()

        if percentage_of_class_passed < 0.25:
            return self.Late.on_time.value

        if percentage_of_class_passed < 0.5:
            return self.Late.half_late.value

        return self.Late.late.value

    def is_absencent(self) -> bool:
        return not self.is_ongoing()


class Calendar:
    def __init__(self) -> None:
        self.classes_schedule = [
            CourseClass(0, time(8, 20), time(12, 00)),  # Monday = 0 (morning)
            CourseClass(0, time(13, 30), time(17, 00)),  # Monday = 0 (afretnoon)
            CourseClass(1, time(8, 20), time(12, 00)),  # Tuesday = 1
            CourseClass(2, time(8, 20), time(12, 00)),  # Wednesday = 2
            CourseClass(3, time(8, 20), time(12, 00)),  # Thursday = 3
            CourseClass(4, time(8, 20), time(12, 00)),  # Friday = 4
            CourseClass(5, time(8, 20), time(12, 00)),  # Saturday = 5
        ]

    def get_current_class(self) -> CourseClass | None:
        for course_class in self.classes_schedule:
            if course_class.is_ongoing():
                return course_class

        return None
