import enum
from datetime import datetime, time, timedelta


class LateTypes(enum.Enum):
    ON_TIME = "sem atraso"
    LATE = "atrasado"


class Weekday(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4


class FirstClassHalf(enum.Enum):
    BEGIN = time(17, 45)
    END = time(20, 00)

    def begin_time_str() -> str:
        return FirstClassHalf.BEGIN.value.strftime("%H:%M")

    def end_time_str() -> str:
        return FirstClassHalf.BEGIN.value.strftime("%H:%M")


class SecondClassHalf(enum.Enum):
    BEGIN = time(20, 15)
    END = time(22, 00)

    def begin_time_str() -> str:
        return SecondClassHalf.BEGIN.value.strftime("%H:%M")

    def end_time_str() -> str:
        return SecondClassHalf.END.value.strftime("%H:%M")


class CourseClass:
    ON_TIME_TOLERANCE = timedelta(seconds=2100)  # 35 minutes

    def __init__(self, weekday: int, start_time: time, end_time: time):
        self.start = datetime.combine(datetime.today(), start_time)
        self.end = datetime.combine(datetime.today(), end_time)
        self.weekday = weekday

    def is_first_half(self) -> bool:
        return self.start.time() == FirstClassHalf.BEGIN.value

    def is_ongoing(self) -> bool:
        if self.weekday == datetime.now().weekday():
            current_time = datetime.now()
            return self.start <= current_time <= self.end
        return False

    def is_late(self):
        is_on_time = datetime.now() - self.start <= self.ON_TIME_TOLERANCE 
        if is_on_time:
            return LateTypes.ON_TIME
        else:
            return LateTypes.LATE

    def is_absent(self) -> bool:
        return not self.is_ongoing()

    def __repr__(self) -> str:
        return f"CourseClass({self.weekday}, {self.start}, {self.end})"


class Schedule:
    def get_current_class(self) -> CourseClass | None:
        MONDAY = [
            CourseClass(Weekday.MONDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value),
            CourseClass(
                Weekday.MONDAY.value, SecondClassHalf.BEGIN.value, SecondClassHalf.END.value
            ),
        ]

        THURSDAY = [
            CourseClass(
                Weekday.THURSDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value
            ),
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
            CourseClass(
                Weekday.TUESDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value
            ),
            CourseClass(
                Weekday.TUESDAY.value,
                SecondClassHalf.BEGIN.value,
                SecondClassHalf.END.value,
            ),
        ]

        FRIDAY = [
            CourseClass(Weekday.FRIDAY.value, FirstClassHalf.BEGIN.value, FirstClassHalf.END.value),
            CourseClass(
                Weekday.FRIDAY.value, SecondClassHalf.BEGIN.value, SecondClassHalf.END.value
            ),
        ]
        CLASSES_SCHEDULE = MONDAY + TUESDAY + WEDNESDAY + THURSDAY + FRIDAY

        classes_schedule = CLASSES_SCHEDULE
        for course_class in classes_schedule:
            if course_class.is_ongoing():
                return course_class

        return None
