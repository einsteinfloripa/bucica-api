import enum
from datetime import datetime, time, timedelta


class Late(enum.Enum):
    ON_TIME = timedelta(seconds=1500)  # 25 minutes
    HALF_LATE = timedelta(seconds=3600)  # 1 hour


class LateTypes(enum.Enum):
    ON_TIME = "sem atraso"
    HALF_LATE = "meio atraso"
    LATE = "atrasado"


class Weekday(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4


class FirstClassHalf(enum.Enum):
    BEGIN = time(17, 50)
    END = time(20, 00)


class SecondClassHalf(enum.Enum):
    BEGIN = time(20, 20)
    END = time(22, 00)


class CourseClass:
    def __init__(self, weekday: int, start_time: time, end_time: time):
        self.start = datetime.combine(datetime.today(), start_time)
        self.end = datetime.combine(datetime.today(), end_time)
        self.weekday = weekday

    def is_first_half(self) -> bool:
        return self.start == FirstClassHalf.BEGIN.value

    def is_ongoing(self) -> bool:
        if self.weekday == datetime.now().weekday():
            current_time = datetime.now()
            return self.start <= current_time <= self.end
        return False

    def is_late(self):
        is_late = datetime.now() - self.start > Late.HALF_LATE.value
        is_half_late = datetime.now() - self.start <= Late.HALF_LATE.value
        is_on_time = datetime.now() - self.start <= Late.ON_TIME.value

        if is_late:
            return LateTypes.LATE

        if is_half_late and not is_on_time:
            return LateTypes.HALF_LATE

        if is_on_time:
            return LateTypes.ON_TIME

    def is_absent(self) -> bool:
        return not self.is_ongoing()

    def __repr__(self) -> str:
        return f"CourseClass({self.weekday}, {self.start}, {self.end})"


class Schedule:
    MONDAY = [
        CourseClass(Weekday.MONDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value),
        CourseClass(Weekday.MONDAY.value, SecondClassHalf.BEGIN.value, SecondClassHalf.END.value),
    ]

    THURSDAY = [
        CourseClass(Weekday.THURSDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value),
        CourseClass(
            Weekday.THURSDAY.value,
            SecondClassHalf.BEGIN.value,
            SecondClassHalf.END.value,
        ),
    ]

    WEDNESDAY = [
        CourseClass(
            Weekday.WEDNESDAY.value,
            FirstClassHalf.BEGIN.value,
            FirstClassHalf.END.value,
        ),
        CourseClass(
            Weekday.WEDNESDAY.value,
            SecondClassHalf.BEGIN.value,
            SecondClassHalf.END.value,
        ),
    ]

    TUESDAY = [
        CourseClass(Weekday.TUESDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value),
        CourseClass(
            Weekday.TUESDAY.value,
            SecondClassHalf.BEGIN.value,
            SecondClassHalf.END.value,
        ),
    ]

    FRIDAY = [
        CourseClass(Weekday.FRIDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value),
        CourseClass(Weekday.FRIDAY.value, SecondClassHalf.BEGIN.value, SecondClassHalf.END.value),
    ]

    CLASSES_SCHEDULE = MONDAY + TUESDAY + WEDNESDAY + THURSDAY + FRIDAY

    def get_current_class(self) -> CourseClass | None:
        classes_schedule = self.CLASSES_SCHEDULE
        for course_class in classes_schedule:
            if course_class.is_ongoing():
                return course_class

        return None