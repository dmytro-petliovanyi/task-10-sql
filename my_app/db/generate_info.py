import re
import string
from random import randint, sample

from my_app.db.models import Course
from my_app.settings.constants import first_names, last_names


def fix_group_name(group_name: str) -> str:
    split_name = group_name.split("-")
    split_name[0] = split_name[0].upper()
    return "-".join(split_name)


def check_group_name(name: str) -> bool:
    pattern = r'^[A-Za-z]{2}-\d{2}$'
    if re.match(pattern, name):
        return True
    else:
        return False


def chose_courses_for_student(query: list[Course]) -> list[Course]:
    return sample(query, randint(1, 3))


def generate_groups(count: int) -> list[str]:
    letters = string.ascii_uppercase
    return [
            f"{letters[randint(0, 25)]}{letters[randint(0, 25)]}-{randint(10, 100)}"
            for _ in range(count)
    ]


def add_students(groups: list[str]) -> list[dict[str, list[dict[str, str]]]]:
    return [{
        group: [
            {
                "first_name": f"{first_names[randint(0, 19)]}",
                "last_name": f"{last_names[randint(0, 19)]}"
            } for _ in range(10, 31)
        ]
    } for group in groups]
