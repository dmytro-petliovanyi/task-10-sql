from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from my_app.db.models import Course, Group, Student
from my_app.db.repository import (CourseRepository, GroupRepository,
                                  StudentRepository)
from my_app.db.scemas import DefaultResponseModel

descriptions = {
    "group_name": "Inappropriate group name. Should be like: XX-00",
    "student_name": "Inappropriate student name. Should contain only letters",
    "group": "Group not found",
    "student": "Student not found",
    "course": "Course not found"
}


response_group_name: dict[int | str, dict[str, Any]] = {
          status.HTTP_422_UNPROCESSABLE_ENTITY: {
              "model": DefaultResponseModel,
              "description": descriptions["group_name"]
          }
}

response_student_name: dict[int | str, dict[str, Any]] = {
          status.HTTP_422_UNPROCESSABLE_ENTITY: {
              "model": DefaultResponseModel,
              "description": descriptions["student_name"]
          }
}

response_group_not_found: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
              "model": DefaultResponseModel,
              "description": descriptions["group"]
    }
}

response_student_not_found: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
              "model": DefaultResponseModel,
              "description": descriptions["student"]
    }
}

response_course_not_found: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
              "model": DefaultResponseModel,
              "description": descriptions["course"]
    }
}


def group_not_found_exc(group_id: int, session: Session) -> Group | None:
    group = GroupRepository(session).get_single(group_id)

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=descriptions["group"]
        )
    return group


def student_not_found_exc(student_id: int, session: Session) -> Student | None:
    student = StudentRepository(session).get_single(student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=descriptions["student"]
        )

    return student


def course_not_found_exc(course_id: int, session: Session) -> Course | None:
    course = CourseRepository(session).get_single(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=descriptions["course"]
        )
    return course
