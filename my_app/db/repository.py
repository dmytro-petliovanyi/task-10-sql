from sqlalchemy.orm import Session

from my_app.db.generate_info import fix_group_name
from my_app.db.models import Course, Group, Student, all_models


class GroupRepository:
    model = all_models[0]

    def __init__(self, session: Session):
        self.session = session

    def get(self) -> list[Group]:
        return self.session.query(self.model).all()

    def get_single(self, group_id: int) -> Group | None:
        return self.session.query(self.model).filter_by(id=group_id).first()

    def delete_group(self, group_id: int) -> None:
        group = self.get_single(group_id)
        if group:
            self.session.delete(group)
            self.session.commit()

    def update_group(self, new_name: str, group_id: int) -> Group | None:
        group = self.get_single(group_id)

        if group:
            group.name = f"{fix_group_name(new_name)}"
            self.session.commit()
            return group

    def create_group(self, group_name: str) -> Group:
        group = self.model(name=fix_group_name(group_name))
        self.session.add(group)
        self.session.commit()
        return group


class StudentRepository:
    model = all_models[1]

    def __init__(self, session: Session):
        self.session = session

    def get(self) -> list[Student]:
        return self.session.query(self.model).all()

    def get_single(self, student_id: int) -> Student | None:
        return self.session.query(self.model).filter_by(id=student_id).first()

    def delete_student(self, student_id: int) -> None:
        student = self.get_single(student_id)
        if student:
            self.session.delete(student)
            self.session.commit()

    def update_student(self,
                       student_id: int,
                       new_group: Group,
                       new_first_name: str,
                       new_last_name: str) -> Student | None:
        new_last_name = new_last_name.capitalize()
        new_first_name = new_first_name.capitalize()

        student = self.get_single(student_id)

        if student:
            student.group = new_group          # type: ignore
            student.first_name = new_first_name
            student.last_name = new_last_name
            self.session.commit()
            return student

    def create_student(self, group: Group, first_name: str, last_name: str) -> Student:
        student = self.model(group=group, first_name=first_name, last_name=last_name)
        self.session.add(student)
        self.session.commit()
        return student


class CourseRepository:
    model = all_models[2]

    def __init__(self, session: Session):
        self.session = session

    def get(self) -> list[Course]:
        return self.session.query(self.model).all()

    def get_single(self, course_id: int) -> Course | None:
        return self.session.query(self.model).filter_by(id=course_id).first()

    def delete_course(self, course_id: int) -> None:
        course = self.get_single(course_id)
        if course:
            self.session.delete(course)
            self.session.commit()

    def update_course(self,
                      course_id: int,
                      new_course_name: str,
                      new_description: str) -> Course | None:
        course = self.get_single(course_id)
        if course:
            course.course_name = new_course_name
            course.description = new_description
            self.session.commit()
            return course

    def create_course(self, course_name: str, description: str) -> Course:
        course = self.model(course_name=course_name, description=description)
        self.session.add(course)
        self.session.commit()
        return course
