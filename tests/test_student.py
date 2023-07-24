from unittest.mock import patch

from fastapi import status

from my_app.db.models import Student
from tests.conftest import (client, mock_courses, mock_student_full,
                            mock_student_with_courses)


@patch("my_app.routers.student_router.StudentRepository.get", return_value=[Student(id=1,
                                                                                    group_id=1,
                                                                                    first_name="John",
                                                                                    last_name="Doe")])
def test_get_student(get_mock):
    response = client.get("/students")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1, "group_id": 1, "first_name": "John", "last_name": "Doe"}]

    get_mock.assert_called_once()


@patch("my_app.routers.student_router.student_not_found_exc", return_value=mock_student_full)
def test_get_single_student(student_not_found_mock):
    response = client.get("/students/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "group_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "courses": []
    }

    student_not_found_mock.assert_called_once()


@patch("my_app.routers.student_router.student_not_found_exc", return_value=Student(id=1,
                                                                                   group_id=1,
                                                                                   first_name="John",
                                                                                   last_name="Doe"))
@patch("my_app.routers.student_router.group_not_found_exc")
@patch("my_app.routers.student_router.StudentRepository.update_student", return_value=Student(id=1,
                                                                                              group_id=1,
                                                                                              first_name="John",
                                                                                              last_name="Doe"))
@patch("my_app.routers.student_router.student_name_exc")
def test_update_student(name_exc_mock, update_mock, group_not_found_mock, student_not_found_mock):
    response = client.put("/students/1", json={"group_id": 1, "first_name": "John", "last_name": "Doe"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "group_id": 1, "first_name": "John", "last_name": "Doe"}

    name_exc_mock.assert_called_once()
    update_mock.assert_called_once()
    group_not_found_mock.assert_called_once()
    student_not_found_mock.assert_called_once()


@patch("my_app.routers.student_router.StudentFullSchema", return_value=mock_student_with_courses)
@patch("my_app.routers.student_router.student_not_found_exc", return_value=Student(id=1,
                                                                                   group_id=1,
                                                                                   first_name="John",
                                                                                   last_name="Doe"))
@patch("my_app.routers.student_router.course_not_found_exc", side_effects=mock_courses)
def test_assign_courses_to_student(course_not_found_mock, student_not_found_mock, student_schema_mock):
    response = client.put("/students/1/courses", json=[{"id": 1}, {"id": 2}])

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_student_with_courses

    course_not_found_mock.assert_called()
    student_not_found_mock.assert_called_once()
    student_schema_mock.assert_called_once()


@patch("my_app.routers.student_router.group_not_found_exc")
@patch("my_app.routers.student_router.StudentRepository.create_student", return_value=Student(id=1,
                                                                                              group_id=1,
                                                                                              first_name="John",
                                                                                              last_name="Doe"))
@patch("my_app.routers.student_router.student_name_exc")
def test_create_student(create_mock, name_exc_mock, group_not_found_mock):
    response = client.post("/students", json={"group_id": 1, "first_name": "John", "last_name": "Doe"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 1, "group_id": 1, "first_name": "John", "last_name": "Doe"}

    create_mock.assert_called_once()
    name_exc_mock.assert_called_once()
    group_not_found_mock.assert_called_once()


@patch("my_app.routers.student_router.student_not_found_exc", return_value=Student(id=1,
                                                                                   group_id=1,
                                                                                   first_name="John",
                                                                                   last_name="Doe"))
@patch("my_app.routers.student_router.StudentRepository.delete_student", return_value={"message": "Student deleted"})
def test_delete_student(delete_mock, student_mock):
    response = client.delete("/students/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Student deleted"}

    delete_mock.assert_called_once()
    student_mock.assert_called_once()
