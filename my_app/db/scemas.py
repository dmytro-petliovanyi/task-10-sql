from pydantic import validator
from pydantic.main import BaseModel

from my_app.db.generate_info import check_group_name, fix_group_name


class AssociationTableSchema(BaseModel):
    id: int
    student_id: int
    course_id: int


class GroupSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CourseSchema(BaseModel):
    id: int
    course_name: str
    description: str

    class Config:
        orm_mode = True


class StudentSchema(BaseModel):
    id: int
    group_id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class StudentFullSchema(BaseModel):
    id: int
    group_id: int
    first_name: str
    last_name: str
    courses: list[CourseSchema]

    class Config:
        orm_mode = True


class GroupFullSchema(BaseModel):
    id: int
    name: str
    students: list[StudentSchema]

    class Config:
        orm_mode = True


class DefaultResponseModel(BaseModel):
    message: str


class RequestGroupSchema(BaseModel):
    name: str

    @validator("name")
    def validate_name(cls, name: str):
        name = name.strip()
        if not check_group_name(name):
            raise ValueError("bad group name, should be like XX-00")

        return fix_group_name(name)


class RequestStudentSchema(BaseModel):
    group_id: int
    first_name: str
    last_name: str

    @validator("first_name")
    def validate_first_name(cls, first_name: str):
        first_name = first_name.strip()
        if not first_name.isalpha():
            raise ValueError("bad first name, should contain only letters")

        return first_name

    @validator("last_name")
    def validate_last_name(cls, last_name: str):
        last_name = last_name.strip()
        if not last_name.isalpha():
            raise ValueError("bad last name, should contain only letters")

        return last_name


class RequestCourseSchema(BaseModel):
    name: str
    description: str

    @validator("name")
    def validate_name(cls, name: str):
        if not name.isalpha():
            raise ValueError("bad name, should contain only letters")

        return name

    @validator("description")
    def validate_description(cls, description: str):

        if not description.isascii():
            raise ValueError("bad description, should contain only letters and symbols")

        return description


class AssignCourseSchema(BaseModel):
    id: int
