from datetime import datetime, time



class DateHandler:
    def __init__(self) -> None:
        self.current_datetime = datetime.now()
    
    def is_today(self, date: datetime) -> bool:
        return date.date() == self.current_datetime.date()
    
    def validate_interval(self, time: time, start: time, end: time) -> bool:
        return start <= time <= end