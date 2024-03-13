from unittest.mock import patch

from my_app.db.generate_info import (add_students, check_group_name,
                                     chose_courses_for_student, fix_group_name,
                                     generate_groups)
from tests.conftest import mock_courses


@patch("my_app.db.generate_info.randint", return_value=2)
@patch("my_app.db.generate_info.sample", return_value=mock_courses)
def test_chose_courses_for_student(sample_mock, randint_mock):
    sample_mock.return_value = mock_courses
    randint_mock.return_value = 2

    result = chose_courses_for_student(mock_courses)

    assert result == [mock_courses[0], mock_courses[1]]
    sample_mock.assert_called_once()
    randint_mock.assert_called_once()


def test_fix_group_name():
    group_name = "xx-00"
    expected_result = "XX-00"

    result = fix_group_name(group_name)

    assert result == expected_result


def test_check_group_name():
    group_name = "AB-12"
    invalid_group_name = "AB-123"

    result = check_group_name(group_name)
    invalid_result = check_group_name(invalid_group_name)

    assert result is True
    assert invalid_result is False


@patch("my_app.db.generate_info.randint", side_effect=3*[0, 0, 99])
def test_generate_groups(randint_mock):
    result = generate_groups(3)

    assert result == ["AA-99", "AA-99", "AA-99"]
    assert randint_mock.call_count == 9


@patch("builtins.range", return_value=range(0, 1))
@patch("my_app.db.generate_info.randint", return_value=0)
def test_add_students(randint_mock, range_mock):
    groups = ["AA-01", "BB-02", "CC-03"]

    result = add_students(groups)

    assert result == [{'AA-01': [{'first_name': 'Adam', 'last_name': 'Smith'}]},
                      {'BB-02': [{'first_name': 'Adam', 'last_name': 'Smith'}]},
                      {'CC-03': [{'first_name': 'Adam', 'last_name': 'Smith'}]}]

    range_mock.assert_called()
    randint_mock.assert_called()
