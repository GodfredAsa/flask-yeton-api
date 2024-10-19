from flask_restful import reqparse

from constants.user_constants import BLANK_ERROR

_item_parser = reqparse.RequestParser()
_item_parser.add_argument("categoryId", type=str, required=True, help=BLANK_ERROR.format("categoryId"))
_item_parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))
_item_parser.add_argument("brand", type=str, required=True, help=BLANK_ERROR.format("brand"))
_item_parser.add_argument("condition", type=str, required=True, help=BLANK_ERROR.format("condition"))
_item_parser.add_argument("model", type=str, required=True, help=BLANK_ERROR.format("model"))
_item_parser.add_argument("price", type=float, required=True, help=BLANK_ERROR.format("price"))
_item_parser.add_argument("cost", type=float, required=True, help=BLANK_ERROR.format("cost"))
_item_parser.add_argument("stock", type=int, required=True, help=BLANK_ERROR.format("stock"))
_item_parser.add_argument("image", type=str, required=True, help=BLANK_ERROR.format("image"))
_item_parser.add_argument("hasVendor", type=bool, required=True, help=BLANK_ERROR.format("hasVendor"))
_item_parser.add_argument("hasGallery", type=bool, required=True, help=BLANK_ERROR.format("hasGallery"))
_item_parser.add_argument("forSale", type=str, required=True, help=BLANK_ERROR.format("selling"))


def item_data():
    return _item_parser.parse_args()