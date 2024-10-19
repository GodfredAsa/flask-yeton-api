from flask_restful import reqparse

from constants.user_constants import BLANK_ERROR

_vendor_parser = reqparse.RequestParser()
_vendor_parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))
_vendor_parser.add_argument("phone", type=str, required=True, help=BLANK_ERROR.format("phone"))
_vendor_parser.add_argument("itemId", type=str, required=True, help=BLANK_ERROR.format("itemId"))


def vendor_data():
    return _vendor_parser.parse_args()
