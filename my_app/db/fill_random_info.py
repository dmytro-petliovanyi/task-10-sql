import typer

from my_app.db.generate_info import (add_students, chose_courses_for_student,
                                     generate_groups)
from my_app.db.repository import (CourseRepository, GroupRepository,
                                  StudentRepository)
from my_app.settings.configs import Base, SessionLocal, engine, logging
from my_app.settings.constants import courses_data

fill_app = typer.Typer()


@fill_app.command("fill")
def fill_tables(group_count: int) -> None:
    groups_data = add_students(generate_groups(group_count))

    with SessionLocal() as session:
        course_repo = CourseRepository(session)
        student_repo = StudentRepository(session)
        group_repo = GroupRepository(session)

        for name, description in courses_data.items():
            course_repo.create_course(name, description)

        courses_query = course_repo.get()

        for group_info in groups_data:
            for group, students in group_info.items():
                group_row = group_repo.create_group(group)

                for student in students:
                    student_row = student_repo.create_student(group_row, student["first_name"], student["last_name"])
                    student_row.courses.extend(chose_courses_for_student(courses_query))
        session.commit()
    logging.info("Tables filled")


@fill_app.command("init")
def init_driver_table() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    logging.info("Tables ready")
