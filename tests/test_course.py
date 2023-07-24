from unittest.mock import patch

from fastapi import status

from tests.conftest import client, mock_courses


@patch("my_app.routers.course_router.CourseRepository.create_course", return_value=mock_courses[0])
def test_create_course(create_mock):
    response = client.post("/courses", json={"name": "Math", "description": "some"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 1, "course_name": "Math", "description": "some"}

    create_mock.assert_called_once()


@patch("my_app.routers.course_router.CourseRepository.get", return_value=mock_courses)
def test_get_courses(get_mock):

    response = client.get("/courses")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": course.id,
                                "course_name": course.course_name,
                                "description": course.description}
                               for course in mock_courses]

    get_mock.assert_called_once()


@patch("my_app.routers.course_router.course_not_found_exc", return_value=mock_courses[0])
def test_get_single_course(not_found_mock):
    response = client.get("/courses/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "course_name": "Math", "description": "some"}

    not_found_mock.assert_called_once()


@patch("my_app.routers.course_router.CourseRepository.update_course", return_value=mock_courses[0])
@patch("my_app.routers.course_router.course_not_found_exc", return_value=mock_courses[0])
def test_update_course(update_mock, not_found_mock):
    response = client.put("/courses/1", json={"name": "Math", "description": "some"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "course_name": "Math", "description": "some"}

    update_mock.assert_called_once()
    not_found_mock.assert_called_once()


@patch("my_app.routers.course_router.CourseRepository.delete_course")
@patch("my_app.routers.course_router.course_not_found_exc", return_value=mock_courses[0])
def test_delete_course(delete_mock, not_found_mock):
    response = client.delete("/courses/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Course deleted"}

    delete_mock.assert_called_once()
    not_found_mock.assert_called_once()
