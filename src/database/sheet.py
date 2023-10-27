import os
from pathlib import Path

import schedule
from gspread import service_account


class AttendanceData:
    def __init__(self, student_id: int, first_half: bool, absence: bool, late: str, created_at: str) -> None:
        self.student_id = student_id
        self.first_half = first_half
        self.absence = absence
        self.late = late
        self.created_at = created_at
    
    def __repr__(self) -> str:
        return f'{self.student_id} {self.first_half} {self.absence} {self.late} {self.created_at}'

class SheetClass:

    def __init__(self, _sheet_id) -> None:
        self.filepath=Path('credentials.json').absolute()
        self.attendance_buffer : list[AttendanceData] = []
        self.sheet_id = _sheet_id

    def push(self, attendance: AttendanceData):
        self.attendance_buffer.append(attendance)

    def update_sheet(self):
        print(f'Updating sheet: {len(self.attendance_buffer)} entries')
        client = service_account(self.filepath)
        spreadsheet = client.open_by_key(self.sheet_id)
        worksheet = spreadsheet.worksheet('Raw')
        
        for attendance in self.attendance_buffer:
            print(attendance)
            worksheet.append_row(
                [ attendance.student_id, attendance.absence, attendance.first_half, attendance.created_at ]
            )
        self.attendance_buffer.clear()


    def update_sheet_schedule(self):
        schedule.every().day.at("22:18").do(self.update_sheet)


SHEET_URL = os.environ.get('SHEET_ID')
Sheet = SheetClass(SHEET_URL)
