import enum
from datetime import datetime, time


class CourseClass:
    class Late(enum.Enum):
        on_time = "on_time"
        half_late = "half_late"
        late = "late"

    def __init__(self, weakday: int, start: time, end: time):
        self.start = self.__start(start)
        self.end = self.__end(end)
        self.lenth = self.end - self.start
        self.weekday = weakday

    def __now(self) -> datetime:
        return datetime.now()

    def __start(self, start: time):
        return datetime.combine(datetime.today(), start)

    def __end(self, end: time):
        return datetime.combine(datetime.today(), end)

    def is_ongoing(self) -> bool:
        print(self.start, self.end)
        if self.weekday == self.__now().weekday():
            current_time = self.__now()
            return self.start <= current_time <= self.end
        return False

    def is_late(self) -> Late:
        pass

    def is_absencent(self) -> bool:
        return not self.is_ongoing()


class Schedule:
    def __init__(self) -> None:
        self.classes_schedule = [
            CourseClass(0, time(8, 20), time(12, 00)),  # Monday = 0 (morning)
            CourseClass(0, time(13, 30), time(23, 00)),  # Monday = 0 (afretnoon)
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
