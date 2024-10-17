from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR

_faq_parser = reqparse.RequestParser()
_faq_parser.add_argument("title", type=str, required=True, help=BLANK_ERROR.format("title"))
_faq_parser.add_argument("message", type=str, required=True, help=BLANK_ERROR.format("message"))


def faq_data():
    return _faq_parser.parse_args()
