
from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR

_category_parser = reqparse.RequestParser()
_category_parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))
_category_parser.add_argument("categoryImageUrl", type=str, required=True, help=BLANK_ERROR.format("categoryImageUrl"))


def category_data():
    return _category_parser.parse_args()
