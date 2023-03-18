import pytest


class TestStudentService:
    def test_student_not_found(self, mocker):
        mocker.patch(
            "src.services.students_service.StudentRepository",
        )
        mocker.patch(
            "src.services.students_service.AttendanceRepository",
        )

    # def test_create_attendance_check_returns_service_result_ok_with_correct_entry(
    #     self, mocker
    # ):
    #     mocker.patch(
    #         "src.services.studants_services.StudantRepository.get_studant",
    #         return_value=self.test_studand,
    #     )
    #     mocker.patch(
    #         "src.utils.schedule.Schedule.get_current_class",
    #         return_value="SOME_CLASS_COURSE_OBJ",
    #     )
    #     mocker.patch(
    #         "src.services.studants_services.StudantRepository.get_attendence",
    #         return_value=None,
    #     )
    #     mocker.patch(
    #         "src.services.studants_services.StudantRepository.create_attendence",
    #         return_value="SUCESSFULLY_CREATED_ATTENDANCE_OBJ",
    #     )

    #     expected = ServiceResult("SUCESSFULLY_CREATED_ATTENDANCE_OBJ")
    #     output = self.tested_service.create_attendance_check("SOME_CPF_KEY")
    #     assert output.value == expected.value

    # def test_create_attendance_check_returns_service_result_studant_not_found_on_invalid_entry(
    #     self, mocker
    # ):
    #     mocker.patch(
    #         "src.services.studants_services.StudantRepository.get_studant",
    #         return_value=None,
    #     )
    #     output = self.tested_service.create_attendance_check("SOME_INVALID_CPF_KEY")
    #     assert isinstance(output.value, AppException.StudentNotFound)

    # def test_create_attendance_check_returns_service_result_ongoing_class_not_found_on_invalid_entry(
    #     self, mocker
    # ):
    #     mocker.patch(
    #         "src.services.studants_services.StudantRepository.get_studant",
    #         return_value=self.test_studand,
    #     )
    #     mocker.patch(
    #         "src.services.studants_services.Schedule.get_current_class",
    #         return_value=None,
    #     )
    #     output = self.tested_service.create_attendance_check("SOME_CPF_KEY")
    #     assert isinstance(output.value, AppException.OngoingClassNotFound)

    # def test_create_attendance_check_returns_service_result_attendance_already_confirmed(
    #     self, mocker
    # ):
    #     mocker.patch(
    #         "src.services.studants_services.StudantRepository.get_studant",
    #         return_value=self.test_studand,
    #     )
    #     mocker.patch(
    #         "src.utils.schedule.Schedule.get_current_class",
    #         return_value="SOME_CLASS_COURSE_OBJ",
    #     )
    #     mocker.patch(
    #         "src.services.studants_services.StudantRepository.get_attendence",
    #         return_value="ALREADY_CREATED_ATTENDANCE_OBJ",
    #     )
    #     output = self.tested_service.create_attendance_check("SOME_CPF_KEY")
    #     assert isinstance(output.value, AppException.AttendanceAlreadyComfimed)

    # ### ServiceResult.get_stutant ###
    # def test_get_student_returns_service_result_ok_with_correct_entry(self, mocker):
    #     mocker.patch(
    #         "src.services.studants_services.StudantRepository.get_studant",
    #         return_value="TEST_VALUE",
    #     )
    #     entry = "TEST_VALUE"
    #     expected = ServiceResult(entry)
    #     output = self.tested_service.get_student(entry)

    #     assert expected.value == output.value

    # def test_get_studant_return_service_result_error_with_invalid_entry(self, mocker):
    #     mocker.patch(
    #         "src.services.studants_services.StudantRepository.get_studant",
    #         return_value=None,
    #     )
    #     entry = None
    #     output = self.tested_service.get_student(entry)

    #     assert isinstance(output.value, AppException.StudentNotFound)
