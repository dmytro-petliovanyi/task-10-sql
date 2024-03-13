from unittest.mock import patch

from my_app.db.models import Course, Group, Student
from my_app.db.repository import (CourseRepository, GroupRepository,
                                  StudentRepository)
from tests.conftest import mock_group, mock_student


@patch("my_app.db.repository.fix_group_name", return_value="XX-00")
def test_create_group(fix_group_name_mock, override_dependency, override_get_db, prepare_db):
    group_repo = GroupRepository(override_get_db)
    group_name = "xx-00"
    result = group_repo.create_group(group_name)

    assert isinstance(result, Group)
    assert result.name == "XX-00"

    fix_group_name_mock.assert_called_once_with(group_name)


def test_get_single(override_dependency, override_get_db, prepare_db):
    group_repo = GroupRepository(override_get_db)

    test_group = Group(id=1, name="Test Group")
    group_repo.session.add(test_group)
    group_repo.session.commit()

    assert test_group == group_repo.get_single(group_id=1)


@patch("my_app.db.repository.GroupRepository.get_single", return_value=mock_group)
@patch("my_app.db.repository.fix_group_name", return_value="AA-01")
def test_update_group(fix_name_mock, mock_get_single, override_dependency, prepare_db, override_get_db):
    group_repo = GroupRepository(override_get_db)

    test_group = Group(id=1, name="Test Group")
    group_repo.session.add(test_group)
    group_repo.session.commit()

    new_name = "AA-01"

    assert new_name == str(group_repo.update_group(new_name=new_name, group_id=1))

    mock_get_single.assert_called_once()
    fix_name_mock.assert_called_once()


@patch("my_app.db.repository.GroupRepository.get_single")
def test_delete_group(mock_get_single, override_dependency, override_get_db, prepare_db):
    group_repo = GroupRepository(override_get_db)

    test_group = Group(id=1, name="Test Group")
    group_repo.session.add(test_group)
    group_repo.session.commit()

    mock_get_single.return_value = test_group

    assert group_repo.delete_group(group_id=1) is None
    assert group_repo.session.query(group_repo.model).filter_by(id=1).first() is None
    mock_get_single.assert_called_once()


def test_create_course(override_dependency, override_get_db, prepare_db):
    course_repo = CourseRepository(override_get_db)
    course_name = "Math"
    description = "some"
    result = course_repo.create_course(course_name, description)

    assert isinstance(result, Course)
    assert result.course_name == "Math"


def test_get_single_course(override_dependency, override_get_db, prepare_db):
    course_repo = CourseRepository(override_get_db)

    test_course = Course(id=1, course_name="Test Course", description="Test Description")
    course_repo.session.add(test_course)
    course_repo.session.commit()

    result = course_repo.get_single(course_id=1)

    assert result == test_course


@patch("my_app.db.repository.CourseRepository.get_single")
def test_delete_course(mock_get_single, override_dependency, override_get_db, prepare_db):
    course_repo = CourseRepository(override_get_db)

    test_course = Course(id=1, course_name="Test Course", description="Test Description")
    course_repo.session.add(test_course)
    course_repo.session.commit()

    mock_get_single.return_value = test_course

    assert course_repo.delete_course(course_id=1) is None
    assert course_repo.session.query(course_repo.model).filter_by(id=1).first() is None

    mock_get_single.assert_called_once()


@patch("my_app.db.repository.CourseRepository.get_single", return_value=mock_group)
def test_update_course(mock_get_single, override_dependency, override_get_db, prepare_db):
    course_repo = CourseRepository(override_get_db)

    test_course = Course(id=1, course_name="Test Course", description="Test Description")
    course_repo.session.add(test_course)
    course_repo.session.commit()

    new_name = "New Course"
    new_description = "gg"
    updated_course = course_repo.update_course(course_id=1, new_course_name=new_name, new_description=new_description)

    assert updated_course.course_name == new_name
    assert updated_course.description == new_description

    course = course_repo.get_single(course_id=1)

    assert course.course_name == new_name
    assert course.description == new_description

    mock_get_single.assert_called()


def test_create_student(override_dependency, override_get_db, prepare_db):
    student_repo = StudentRepository(override_get_db)
    first_name = "John"
    last_name = "Doe"
    group = Group(id=1, name="Test Group")

    result = student_repo.create_student(group=group, first_name=first_name, last_name=last_name)

    assert isinstance(result, Student)
    assert result.first_name == first_name
    assert result.last_name == last_name
    assert result.group == group


def test_get_single_student(override_dependency, override_get_db, prepare_db):
    student_repo = StudentRepository(override_get_db)

    test_student = Student(id=1, first_name="John", last_name="Doe", group=Group(name="Test Group"))
    student_repo.session.add(test_student)
    student_repo.session.commit()

    assert test_student == student_repo.get_single(student_id=1)


@patch("my_app.db.repository.StudentRepository.get_single", return_value=mock_student)
def test_update_student(mock_get_single, override_dependency, override_get_db, prepare_db):
    student_repo = StudentRepository(override_get_db)

    test_student = Student(id=1, first_name="John", last_name="Doe", group=Group(name="Test Group"))
    student_repo.session.add(test_student)
    student_repo.session.commit()

    new_group = Group(name="New Group")
    new_first_name = "Jane"
    new_last_name = "Smith"

    assert f"{new_first_name} {new_last_name}" == str(
        student_repo.update_student(student_id=1, new_group=new_group, new_first_name=new_first_name,
                                    new_last_name=new_last_name))

    mock_get_single.assert_called_once()


@patch("my_app.db.repository.StudentRepository.get_single")
def test_delete_student(mock_get_single, override_dependency, override_get_db, prepare_db):
    student_repo = StudentRepository(override_get_db)

    test_student = Student(id=1, first_name="John", last_name="Doe", group=Group(name="Test Group"))
    student_repo.session.add(test_student)
    student_repo.session.commit()

    mock_get_single.return_value = test_student

    assert student_repo.delete_student(student_id=1) is None
    assert student_repo.session.query(student_repo.model).filter_by(id=1).first() is None

    mock_get_single.assert_called_once()
