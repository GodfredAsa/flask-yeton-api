import uuid
from datetime import datetime
import random
import string


def generate_uuid():
    return str(uuid.uuid4())


def format_created_date():
    created_date = datetime.today()
    return f"{created_date.day}-{created_date.month}-{created_date.year}"


def return_message(status: int, message: str) -> object:
    return {'status': status, 'message': message}


def generate_unique_code() -> str:
    return generate_random_letters(4) + \
           generate_random_numbers(3) +\
           generate_random_letters(2) + \
           generate_random_numbers(4)


def generate_random_letters(num: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase, k=num))


def generate_random_numbers(num: int) -> str:
    return ''.join(random.choices(string.digits, k=num))


def str_to_bool(value):
    if isinstance(value, str):
        return value.lower() == 'true'
    return bool(value)