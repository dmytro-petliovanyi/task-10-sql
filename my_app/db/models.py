from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from my_app.settings.configs import Base


class AssociationTable(Base):
    __tablename__ = 'user_course'
    id: Mapped[int] = Column(Integer, primary_key=True)
    student_id: Mapped[int] = Column(Integer, ForeignKey('students.id'))
    course_id: Mapped[int] = Column(Integer, ForeignKey('courses.id'))


class Course(Base):
    __tablename__ = 'courses'
    id: Mapped[int] = Column(Integer, primary_key=True)
    course_name: Mapped[str] = Column(String(50), nullable=False)
    description: Mapped[str] = Column(String(255), nullable=False)

    def __str__(self) -> str:
        return self.course_name


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = Column(Integer, primary_key=True)
    group_id: Mapped[int] = Column(Integer, ForeignKey('groups.id'))
    first_name: Mapped[str] = Column(String(120), nullable=False)
    last_name: Mapped[str] = Column(String(120), nullable=False)
    courses: Mapped[list[Course]] = relationship("Course", secondary='user_course', backref='students', lazy='dynamic')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    students: Mapped[list[Student]] = relationship("Student", backref='group')

    def __str__(self) -> str:
        return self.name


all_models = [Group, Student, Course, AssociationTable]
