from unittest.mock import patch

from fastapi import status

from tests.conftest import client, mock_group, mock_group_full


@patch("my_app.routers.group_router.group_name_exc")
@patch("my_app.routers.group_router.GroupRepository.create_group", return_value=mock_group)
def test_create_group(create_mock, name_exc_mock):
    response = client.post("/groups", json={"name": "XX-00"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 1, "name": "XX-00"}

    create_mock.assert_called_once()
    name_exc_mock.assert_called_once()


@patch("my_app.routers.group_router.GroupRepository.get", return_value=[mock_group])
def test_get_group(get_mock):

    response = client.get("/groups")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1, "name": "XX-00"}]

    get_mock.assert_called_once()


@patch("my_app.routers.group_router.group_not_found_exc", return_value=mock_group_full)
def test_get_single_group(not_found_mock):
    response = client.get("/groups/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "name": "XX-00", "students": []}

    not_found_mock.assert_called_once()


@patch("my_app.routers.group_router.group_name_exc")
@patch("my_app.routers.group_router.group_not_found_exc", return_value=mock_group)
@patch("my_app.routers.group_router.GroupRepository.update_group", return_value={"id": 1, "name": "XX-11"})
def test_update_group(update_mock, not_found_mock, name_exc_mock):

    response = client.put("/groups/1", json={"name": "XX-11"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "name": "XX-11"}

    update_mock.assert_called_once()
    name_exc_mock.assert_called_once()
    not_found_mock.assert_called_once()


@patch("my_app.routers.group_router.StudentRepository.delete_student")
@patch("my_app.routers.group_router.group_not_found_exc", return_value=mock_group)
@patch("my_app.routers.group_router.GroupRepository.delete_group", return_value={"message": "Group deleted"})
def test_delete_group(delete_group_mock, not_found_exc_mock, delete_student_mock):
    response = client.delete("/groups/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Group and associated students deleted"}

    not_found_exc_mock.assert_called_once()
    delete_group_mock.assert_called_once()
