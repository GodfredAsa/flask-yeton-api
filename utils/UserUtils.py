import re
import bcrypt
from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR
from model.User import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))
# _user_parser.add_argument("email", type=str, help=BLANK_ERROR.format("email"))
_user_parser.add_argument("imageUrl", type=str, help=BLANK_ERROR.format("imageUrl"))
_user_parser.add_argument("phone", type=str, required=True, help=BLANK_ERROR.format("phone"))
_user_parser.add_argument("gender", type=str, help=BLANK_ERROR.format("gender"))
_user_parser.add_argument("password", type=str, required=True, help=BLANK_ERROR.format("password"))


def user_data():
    return _user_parser.parse_args()


def user_exist_by_email(email):
    return False if not UserModel.find_by_email(email) else True


def user_exist_by_phone(phone):
    return False if not UserModel.find_by_phone(phone) else True


def verify_credentials(phone, password):
    if not UserModel.find_by_phone(phone):
        return False
    hashed_password = UserModel.find_by_phone(phone).password
    return True \
        if bcrypt.hashpw(password.encode('utf-8'), hashed_password) == hashed_password \
        else False


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    pattern = r'^0[2-9][0-9]{8}$'
    return re.match(pattern, phone) is not None


# def generate_token(user: 'UserModel') -> str:
#     return create_refresh_token(user.phone_number) \
#         if user.is_admin \
#         else create_access_token(identity=user.phone_number)

def generate_token(user: 'UserModel') -> str:
    return user.phone_number
