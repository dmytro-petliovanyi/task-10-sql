from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from my_app.db.models import Course
from my_app.db.repository import CourseRepository
from my_app.db.scemas import (CourseSchema, DefaultResponseModel,
                              RequestCourseSchema)
from my_app.routers.dependencies import (course_not_found_exc,
                                         response_course_not_found)
from my_app.settings.configs import get_db

course_router = APIRouter()


@course_router.get("/courses", response_model=list[CourseSchema])
@cache(expire=60)
async def get_courses(session: Session = Depends(get_db)) -> list[Course]:
    return CourseRepository(session).get()


@course_router.get("/courses/{course_id}", response_model=Union[CourseSchema, None],
                   responses=response_course_not_found)
@cache(expire=60)
async def get_single_course(course_id: int, session: Session = Depends(get_db)) -> Course | None:
    return course_not_found_exc(course_id, session)


@course_router.put("/courses/{course_id}", response_model=Union[CourseSchema, None],
                   responses=response_course_not_found)
async def update_course(course_id: int,
                        request: RequestCourseSchema,
                        session: Session = Depends(get_db)) -> Course | None:
    course_repo = CourseRepository(session)

    course = course_not_found_exc(course_id, session)

    if course:

        new_course_name = request.name
        new_description = request.description

        return course_repo.update_course(
            course_id,
            new_course_name,
            new_description,
        )


@course_router.post("/courses", response_model=CourseSchema, status_code=status.HTTP_201_CREATED)
async def create_course(request: RequestCourseSchema, session: Session = Depends(get_db)) -> Course:
    course_repo = CourseRepository(session)

    course_name = request.name
    description = request.description

    return course_repo.create_course(course_name, description)


@course_router.delete("/courses/{course_id}", response_model=Union[DefaultResponseModel, None],
                      responses=response_course_not_found)
async def delete_course(course_id: int, session: Session = Depends(get_db)) -> dict[str, str] | None:
    course_repo = CourseRepository(session)
    course = course_not_found_exc(course_id, session)
    if course:
        course_repo.delete_course(course_id)
        return {"message": "Course deleted"}
