import os
import json
import schedule

from pathlib import Path
from dataclasses import dataclass
from gspread import service_account_from_dict

@dataclass
class AttendanceData:
    student_id: int
    first_half: bool
    absence: bool
    late: str
    created_at: str

class SheetClass:

    __attendance_buffer = []
    __sheet_id = os.environ.get('SHEET_ID')

    # Public methods
    @classmethod
    def push_attendance(cls, attendance: AttendanceData):
        cls.__attendance_buffer.append(attendance)

    @classmethod
    def update_sheet_schedule(cls):
        schedule.every().day.at("22:30").do(cls.__update_sheet)

    # Private methods
    @staticmethod
    def __get_credentials():
        with open('account.json', 'r') as f:
            creeds = json.load(f)
        creeds.update({"private_key": os.environ.get('PRIVATE_KEY').replace('\\n', '\n')})
        creeds.update({"private_key_id": os.environ.get('PRIVATE_KEY_ID')})
        return creeds


    @classmethod
    def __update_sheet(cls):
        print(f'Updating sheet: {len(cls.__attendance_buffer)} entries')
        creeds = cls.__get_credentials()
        client = service_account_from_dict(creeds)
        spreadsheet = client.open_by_key(cls.__sheet_id)
        worksheet = spreadsheet.worksheet('Raw')
        
        for attendance in cls.__attendance_buffer:
            print(attendance)
            worksheet.append_row(
                [ attendance.late , attendance.student_id, attendance.absence, attendance.created_at, attendance.first_half ]
            )
        cls.__attendance_buffer.clear()

Sheet = SheetClass()
