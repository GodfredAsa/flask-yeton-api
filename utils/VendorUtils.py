from flask_restful import reqparse

from constants.user_constants import BLANK_ERROR

_vendor_parser = reqparse.RequestParser()
_vendor_parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))
_vendor_parser.add_argument("phone", type=str, required=True, help=BLANK_ERROR.format("phone"))


def vendor_data():
    return _vendor_parser.parse_args()


_assign_item_parser = reqparse.RequestParser()


_assign_item_parser.add_argument("itemId", type=str, required=True, help=BLANK_ERROR.format("itemId"))


def assign_item_vendor_data():
    return _assign_item_parser.parse_args()

