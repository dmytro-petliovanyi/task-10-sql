from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from my_app.db.models import Student
from my_app.db.repository import StudentRepository
from my_app.db.scemas import (AssignCourseSchema, CourseSchema,
                              DefaultResponseModel, RequestStudentSchema,
                              StudentFullSchema, StudentSchema)
from my_app.routers.dependencies import (course_not_found_exc,
                                         group_not_found_exc,
                                         response_course_not_found,
                                         response_group_not_found,
                                         response_student_name,
                                         response_student_not_found,
                                         student_not_found_exc)
from my_app.settings.configs import get_db

student_router = APIRouter()


@student_router.get("/students", response_model=list[StudentSchema])
@cache(expire=60)
async def get_student(session: Session = Depends(get_db)) -> list[Student]:
    return StudentRepository(session).get()


@student_router.get("/students/{student_id}", response_model=Union[StudentFullSchema, None],
                    responses=response_student_not_found)
@cache(expire=60)
async def get_single_student(student_id: int, session: Session = Depends(get_db)) -> StudentFullSchema | None:
    student = student_not_found_exc(student_id, session)

    if student:
        courses = [CourseSchema(id=course.id,
                                course_name=course.course_name,
                                description=course.description) for course in student.courses]

        return StudentFullSchema(
            id=student.id,
            group_id=student.group_id,
            first_name=student.first_name,
            last_name=student.last_name,
            courses=courses
        )


@student_router.put("/students/{student_id}",
                    response_model=Union[StudentSchema, None],
                    responses={**response_student_not_found, **response_group_not_found, **response_student_name})
async def update_student(student_id: int,
                         request: RequestStudentSchema,
                         session: Session = Depends(get_db)) -> Student | None:
    student_repo = StudentRepository(session)

    new_group_id = request.group_id
    student_new_first_name = request.first_name
    student_new_last_name = request.last_name

    student = student_not_found_exc(student_id, session)
    if student:
        new_group = group_not_found_exc(new_group_id, session)

        if new_group:
            return student_repo.update_student(
                student_id,
                new_group,
                student_new_first_name,
                student_new_last_name,
            )


@student_router.put("/students/{student_id}/courses",
                    response_model=Union[StudentFullSchema, None],
                    responses={**response_student_not_found, **response_course_not_found})
async def assign_courses_to_student(student_id: int,
                                    request: list[AssignCourseSchema],
                                    session: Session = Depends(get_db)) -> StudentFullSchema | None:
    student = student_not_found_exc(student_id, session)
    if student:
        courses_ids = [course.id for course in request]

        for course_id in courses_ids:
            course = course_not_found_exc(course_id, session)
            if course not in student.courses and course:
                student.courses.append(course)

        session.commit()

        courses = [CourseSchema(id=course.id,
                                course_name=course.course_name,
                                description=course.description) for course in student.courses]

        return StudentFullSchema(
            id=student.id,
            group_id=student.group_id,
            first_name=student.first_name,
            last_name=student.last_name,
            courses=courses
        )


@student_router.post("/students",
                     response_model=Union[StudentSchema, None],
                     status_code=status.HTTP_201_CREATED,
                     responses={**response_group_not_found, **response_student_name})
async def create_student(request: RequestStudentSchema, session: Session = Depends(get_db)) -> Student | None:
    student_repo = StudentRepository(session)

    group_id = request.group_id
    student_new_first_name = request.first_name
    student_new_last_name = request.last_name

    group = group_not_found_exc(group_id, session)

    if group:
        return student_repo.create_student(group, student_new_first_name, student_new_last_name)


@student_router.delete("/students/{student_id}",
                       response_model=Union[DefaultResponseModel, None],
                       responses=response_student_not_found)
async def delete_student(student_id: int, session: Session = Depends(get_db)) -> dict[str, str] | None:
    student_repo = StudentRepository(session)

    student = student_not_found_exc(student_id, session)
    if student:
        student_repo.delete_student(student_id)
        return {"message": "Student deleted"}
