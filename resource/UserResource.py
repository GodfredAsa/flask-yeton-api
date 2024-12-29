import bcrypt
from flask_jwt_extended import jwt_required, jwt_refresh_token_required
from flask_restful import Resource
from flask import request
import http.client as status
from constants.user_constants import USER_ALREADY_EXISTS, INVALID_EMAIL, ATTRIBUTE_ERROR, USER_NOT_REGISTERED, \
    USER_ALREADY_EXISTS_BY_PHONE
from model.User import UserModel
from utils.UserUtils import user_data, user_exist_by_email, user_exist_by_phone, validate_phone, validate_email, verify_credentials, \
    generate_token
from utils.GeneralUtils import return_message


class UserRegistrationResource(Resource):
    @classmethod
    def post(cls):
        data = user_data()
        try:
            if not validate_phone(data['phone']):
                return return_message(status.BAD_REQUEST, "Invalid Phone Number"), status.BAD_REQUEST

            if user_exist_by_phone(data['phone']):
                return return_message(status.BAD_REQUEST, USER_ALREADY_EXISTS_BY_PHONE), status.BAD_REQUEST
            if data['password'].strip() == "":
                return return_message(status.BAD_REQUEST, "Password cannot be empty"), status.BAD_REQUEST
            user = UserModel(**data)
            user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
            user.save_to_db()
            return user.json(), status.CREATED
        except AttributeError as e:
            print(ATTRIBUTE_ERROR.format(e))
            return return_message(status.BAD_REQUEST, USER_NOT_REGISTERED), status.BAD_REQUEST


class AdminUserResource(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        data = user_data()
        print(data)
        try:
            # if user_exist_by_email(data['email']):
            #     return return_message(status.BAD_REQUEST, USER_ALREADY_EXISTS), status.BAD_REQUEST
            if not validate_phone(data['phone']):
                return return_message(status.BAD_REQUEST, "Invalid Phone Number"), status.BAD_REQUEST
            if user_exist_by_phone(data['phone']):
                return return_message(status.BAD_REQUEST, USER_ALREADY_EXISTS_BY_PHONE), status.BAD_REQUEST
            user = UserModel(**data)
            # if not validate_email(user.email):
            #     return return_message(status.BAD_REQUEST, INVALID_EMAIL), status.BAD_REQUEST
            user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
            user.is_admin = True
            user.save_to_db()
            return user.json(), status.CREATED
        except AttributeError as e:
            print(ATTRIBUTE_ERROR.format(e))
            return return_message(status.BAD_REQUEST, "Admin not added"), status.BAD_REQUEST

    @classmethod
    @jwt_refresh_token_required
    def get(cls):
        return [user.json() for user in UserModel.find_all_users()]


class BlackListUserResource(Resource):
    @jwt_refresh_token_required
    def put(self, phone):
        user = UserModel.find_by_phone(phone)
        if not user:
            return return_message(status.BAD_REQUEST, "User not found"), status.BAD_REQUEST
        isBlackListed = False if user.isBlackListed else True
        user.isBlackListed = isBlackListed
        user.save_to_db()
        return return_message(
            status.OK,
            f"User with {phone} account blocked"
            if isBlackListed
            else f"User with {phone} account activated"
        )

    @jwt_refresh_token_required
    def get(self, phone):
        user = UserModel.find_by_phone(phone)
        if not user:
            return return_message(status.BAD_REQUEST, "User not found"), status.BAD_REQUEST
        if not user.is_admin:
            return return_message(status.UNAUTHORIZED, "Not enough permission"), status.UNAUTHORIZED
        return [user.json() for user in UserModel.find_all_users() if user.isBlackListed], status.OK


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        if not verify_credentials(data['phone'], data['password']):
            return return_message(status.BAD_REQUEST, "Invalid login credentials"), status.BAD_REQUEST
        user = UserModel.find_by_phone(data["phone"])
        if user.isBlackListed:
            return return_message(status.BAD_REQUEST, "Your account is blocked. Please contact support"), status.BAD_REQUEST
        user.isOnline = True
        user.save_to_db()
        return {
            'message': "Login successfully",
            "token": generate_token(user),
            'user': user.json()
        }, status.OK


class LogoutUser(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        user = UserModel.find_by_phone(data['phone'])
        if not user:
            return return_message(status.BAD_REQUEST, "User Not found"), status.BAD_REQUEST
        if not user.isOnline:
            return return_message(status.BAD_REQUEST, "You are not logged in"), status.BAD_REQUEST
        user.isOnline = False
        user.save_to_db()
        return {
            'message': "Logout successfully",
            "token": None
        }, status.OK

