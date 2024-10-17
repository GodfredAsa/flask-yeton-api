from flask_restful import reqparse

from constants.user_constants import BLANK_ERROR

_gallery_parser = reqparse.RequestParser()
_gallery_parser.add_argument("itemId", type=str, required=True, help=BLANK_ERROR.format("image"))
_gallery_parser.add_argument("image", type=str, required=True, help=BLANK_ERROR.format("image"))


def gallery_data():
    return _gallery_parser.parse_args()