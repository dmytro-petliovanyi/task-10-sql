import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from my_app.api import app
from my_app.db.models import Course, Group, Student
from my_app.settings.configs import Base, get_db

mock_group = Group(id=1, name="XX-00")
mock_student = Student(id=1, group_id=1, first_name="John", last_name="Doe")
mock_group_full = Group(id=1, name="XX-00", students=[])
mock_courses = [Course(id=1, course_name="Math", description="some"),
                Course(id=2, course_name="Science", description="some")]
mock_student_full = Student(id=1, group_id=1, first_name="John", last_name="Doe", courses=[])
mock_student_with_courses = {"id": 1,
                             "group_id": 1,
                             "first_name": "John",
                             "last_name": "Doe",
                             "courses": [{"id": course.id,
                                          "course_name": course.course_name,
                                          "description": course.description}
                                         for course in mock_courses]}

POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def override_get_db():
    connection = engine.connect()

    transaction = connection.begin()

    db = TestingSessionLocal(bind=connection)

    yield db

    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def prepare_db():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def override_dependency():
    app.dependency_overrides[get_db] = override_get_db
    yield
    del app.dependency_overrides[get_db]


client = TestClient(app)
