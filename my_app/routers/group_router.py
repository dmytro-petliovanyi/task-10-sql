from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from my_app.db.models import Group
from my_app.db.repository import GroupRepository, StudentRepository
from my_app.db.scemas import (DefaultResponseModel, GroupFullSchema,
                              GroupSchema, RequestGroupSchema, StudentSchema)
from my_app.routers.dependencies import (group_not_found_exc,
                                         response_group_name,
                                         response_group_not_found)
from my_app.settings.configs import get_db

group_router = APIRouter()


@group_router.get("/groups", response_model=list[GroupSchema])
@cache(expire=60)
async def get_group(session: Session = Depends(get_db)) -> list[Group]:
    return GroupRepository(session).get()


@group_router.get("/groups/{group_id}", response_model=Union[GroupFullSchema, None], responses=response_group_not_found)
@cache(expire=60)
async def get_single_group(group_id: int, session: Session = Depends(get_db)) -> GroupFullSchema | None:
    group = group_not_found_exc(group_id, session)
    if group:
        students = [StudentSchema(id=student.id,
                                  group_id=student.group_id,
                                  first_name=student.first_name,
                                  last_name=student.last_name) for student in group.students]

        return GroupFullSchema(id=group.id,
                               name=group.name,
                               students=students)


@group_router.put("/groups/{group_id}",
                  response_model=Union[GroupSchema, None],
                  responses={**response_group_not_found, **response_group_name})
async def update_group(group_id: int, request: RequestGroupSchema, session: Session = Depends(get_db)) -> Group | None:
    group_repo = GroupRepository(session)

    new_group_name = request.name

    group_not_found_exc(group_id, session)

    return group_repo.update_group(group_id=group_id, new_name=new_group_name)


@group_router.post("/groups", response_model=Union[GroupSchema, None],
                   status_code=status.HTTP_201_CREATED,
                   responses=response_group_name)
async def create_group(request: RequestGroupSchema, session: Session = Depends(get_db)) -> Group | None:
    group_repo = GroupRepository(session)

    group_name = request.name

    created_group = group_repo.create_group(group_name)
    return created_group


@group_router.delete("/groups/{group_id}", response_model=Union[DefaultResponseModel, None],
                     responses=response_group_not_found)
async def delete_group(group_id: int, session: Session = Depends(get_db)) -> dict[str, str] | None:
    group_repo = GroupRepository(session)
    student_repo = StudentRepository(session)

    group = group_not_found_exc(group_id, session)
    if group:
        students = group.students

        for student in students:
            student_repo.delete_student(student.id)

        group_repo.delete_group(group_id)

        return {"message": "Group and associated students deleted"}
