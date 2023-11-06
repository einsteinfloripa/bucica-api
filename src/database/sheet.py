import os
import json
import schedule

from pathlib import Path
from gspread import service_account_from_dict



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
        self.attendance_buffer : list[AttendanceData] = []
        self.sheet_id = _sheet_id

    def push_attendance(self, attendance: AttendanceData):
        self.attendance_buffer.append(attendance)

    def update_sheet(self):
        print(f'Updating sheet: {len(self.attendance_buffer)} entries')
        creeds = self.__get_credentials()
        client = service_account_from_dict(creeds)
        spreadsheet = client.open_by_key(self.sheet_id)
        worksheet = spreadsheet.worksheet('Raw')
        
        for attendance in self.attendance_buffer:
            print(attendance)
            worksheet.append_row(
                [ attendance.late , attendance.student_id, attendance.absence, attendance.created_at, attendance.first_half ]
            )
        self.attendance_buffer.clear()


    def update_sheet_schedule(self):
        schedule.every().day.at("22:30").do(self.update_sheet)

    def __get_credentials(self):
        with open('account.json', 'r') as f:
            creeds = json.load(f)
        creeds.update({"private_key": os.environ.get('PRIVATE_KEY').replace('\\n', '\n')})
        creeds.update({"private_key_id": os.environ.get('PRIVATE_KEY_ID')})
        return creeds


SHEET_URL = os.environ.get('SHEET_ID')
Sheet = SheetClass(SHEET_URL)
