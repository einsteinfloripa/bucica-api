from workalendar.america import BrazilSantaCatarina
from datetime import datetime, time


class DateHandler:

    work_calendar = BrazilSantaCatarina()

    def __init__(self) -> None:
        self.current_datetime = datetime.now()
    
    def is_today(self, date: datetime) -> bool:
        return date.date() == self.current_datetime.date()
    
    def is_holiday(self, date_time: datetime) -> bool:
        '''
        this function checks the following holidays:
            (datetime.date(2023, 1, 1), 'New year')
            (datetime.date(2023, 4, 9), 'Easter Sunday')
            (datetime.date(2023, 4, 21), "Tiradentes' Day")
            (datetime.date(2023, 5, 1), 'Labour Day')
            (datetime.date(2023, 8, 11), 'Criação da capitania, separando-se de SP')
            (datetime.date(2023, 9, 7), 'Independence Day')
            (datetime.date(2023, 10, 12), 'Our Lady of Aparecida')
            (datetime.date(2023, 11, 2), "All Souls' Day")
            (datetime.date(2023, 11, 15), 'Republic Day')
            (datetime.date(2023, 11, 25), 'Dia de Santa Catarina de Alexandria')
            (datetime.date(2023, 12, 25), 'Christmas Day')
        '''
        return self.work_calendar.is_holiday(date_time)