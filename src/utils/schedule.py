import enum
from datetime import datetime, time, timedelta


class Late(enum.Enum):
    on_time = timedelta(seconds=1500)  # 25 minutes
    half_late = timedelta(seconds=3600)  # 1 hour


class LateTypes(enum.Enum):
    on_time = "on_time"
    half_late = "half_late"
    late = "late"


class Weekday(enum.Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4


class FirstClassHalf(enum.Enum):
    begin = time(17, 50)
    end = time(20, 00)


class SecondClassHalf(enum.Enum):
    begin = time(20, 20)
    end = time(22, 00)


class CourseClass:
    def __init__(self, weekday: int, start: time, end: time):
        self.start = datetime.combine(datetime.today(), start)
        self.end = datetime.combine(datetime.today(), end)
        self.weekday = weekday

    def is_ongoing(self) -> bool:
        if self.weekday == datetime.now().weekday():
            current_time = datetime.now()
            return self.start <= current_time <= self.end
        return False

    def is_late(self) -> Late:
        is_late = datetime.now() - self.start > Late.half_late.value
        is_half_late = datetime.now() - self.start <= Late.half_late.value
        is_on_time = datetime.now() - self.start <= Late.on_time.value

        if is_late:
            return "atrasado"
        elif is_half_late and not is_on_time:
            return "meio atraso"
        elif is_on_time:
            return "sem atraso"

    def is_absent(self) -> bool:
        return not self.is_ongoing()


class Schedule:
    def get_current_class(self) -> CourseClass | None:
        classes_schedule = self.CLASSES_SCHEDULE

        for course_class in classes_schedule:
            if course_class.is_ongoing():
                return course_class

        return None
