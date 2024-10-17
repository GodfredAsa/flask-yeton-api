from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR

_address_parser = reqparse.RequestParser()
_address_parser.add_argument("userId", type=str, required=True, help=BLANK_ERROR.format("userId"))
_address_parser.add_argument("regionId", type=str, help=BLANK_ERROR.format("regionId"))
_address_parser.add_argument("location", type=str, help=BLANK_ERROR.format("location"))


def get_address_data():
    return _address_parser.parse_args()
