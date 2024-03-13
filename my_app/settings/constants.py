import os
from enum import Enum

POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")


SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"


class SizeEnum(str, Enum):
    full = "full"


courses_data = {
    "math": "Learn advanced algebra and calculus",
    "biology": "Explore the world of living organisms",
    "chemistry": "Study the properties of matter and chemical reactions",
    "history": "Discover the events and people that shaped the world",
    "computer science": "Learn programming and software development",
    "art": "Develop your creative skills and explore different art styles",
    "literature": "Read and analyze classic and modern works of fiction",
    "physics": "Explore the laws of nature and the behavior of matter and energy",
    "economics": "Understand the principles of production, distribution, and consumption of goods and services",
    "psychology": "Study the human mind and behavior"
}

first_names = ['Adam', 'Oliver', 'Liam', 'Noah', 'Ethan', 'Aiden', 'Mia', 'Emma', 'Olivia',
               'Ava', 'Sophia', 'Isabella', 'Charlotte',
               'Amelia', 'Harper', 'Evelyn', 'Abigail', 'Emily', 'Elizabeth', 'Ella']

last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Garcia',
              'Martinez', 'Miller', 'Davis', 'Rodriguez', 'Hernandez', 'Turner', 'Scott',
              'Cooper', 'Carter', 'Reed', 'Stewart', 'Morris', 'Watson']
