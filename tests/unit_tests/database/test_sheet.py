import os
import pytest
import gspread

from faker import Faker
from pytest_mock import MockerFixture
from src.database.sheet import SheetClass, AttendanceData


@pytest.fixture
def clear_sheet_attendance():
    SheetClass._SheetClass__attendance_buffer = []

@pytest.mark.unit
@pytest.mark.sheet
@pytest.mark.usefixtures("clear_sheet_attendance")
class Test_SheetClass:
    EXPECTED_CREDS_DICT = {
        "private_key_id":"some_value",
        "private_key":"some_value"
    }
    MOCKED_BUFFER = [
        AttendanceData(
            student_id=1,
            first_half=True,
            absence=False,
            late="some_value",
            created_at="some_value"
        ),
        AttendanceData(
            student_id=2,
            first_half=False,
            absence=True,
            late="some_value",
            created_at="some_value"
        )
    ]

    def test_push_attendance(self, mocker: MockerFixture):
        assert SheetClass._SheetClass__attendance_buffer == []
        SheetClass.push_attendance("some_value")
        assert SheetClass._SheetClass__attendance_buffer == ["some_value"]
        SheetClass.push_attendance("other_value")
        assert SheetClass._SheetClass__attendance_buffer == ["some_value", "other_value"]


    def test_update_sheet_schedule(self, mocker: MockerFixture):
        mock_every = mocker.patch('schedule.every')

        SheetClass.update_sheet_schedule()

        mock_every().day.at.assert_called_once_with("22:30")
        mock_every().day.at().do.assert_called_once_with(SheetClass._SheetClass__update_sheet)


    def test_get_credentials(self, mocker: MockerFixture):
        mocker.patch('json.load', return_value={})
        mocker.patch('os.environ.get', return_value="some_value")

        creeds = SheetClass._SheetClass__get_credentials()
        
        assert creeds == self.EXPECTED_CREDS_DICT


    def test_update_sheet(self, mocker: MockerFixture):

        mocker.patch.object(SheetClass, '_SheetClass__attendance_buffer', self.MOCKED_BUFFER)
        mocker.patch('src.database.sheet.SheetClass._SheetClass__get_credentials', return_value=[])
        mock_print = mocker.patch('builtins.print')

        worksheet_mock = mocker.Mock(append_rows=mocker.Mock())
        spreadsheet_mock = mocker.Mock(worksheet=mocker.Mock(return_value=worksheet_mock))
        client_mock = mocker.Mock(open_by_key=mocker.Mock(return_value=spreadsheet_mock))
        mocker.patch('src.database.sheet.service_account_from_dict', return_value=client_mock)

        SheetClass._SheetClass__update_sheet()

        assert client_mock.open_by_key.call_count == 1
        assert worksheet_mock.append_rows.call_count == 1
        assert worksheet_mock.append_rows.call_args[0][0] == [
            ['some_value', 1, False, 'some_value', True],
            ['some_value', 2, True, 'some_value', False]
        ]
        
        # one for the header and one for each attendance
        assert mock_print.call_count == 3
        

