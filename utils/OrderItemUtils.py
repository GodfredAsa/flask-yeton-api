from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR
from model.Item import ItemModel

_order_parser = reqparse.RequestParser()
_order_parser.add_argument("qty", type=int, required=True, help=BLANK_ERROR.format("qty"))
_order_parser.add_argument("userId", type=str, required=True, help=BLANK_ERROR.format("qty"))
_order_parser.add_argument("itemId", type=str, required=True, help=BLANK_ERROR.format("itemId"))


def order_data():
    return _order_parser.parse_args()


def getItemName(itemId: str) -> str:
    return ItemModel.find_by_uuid(itemId).name if ItemModel.find_by_uuid(itemId) else "NO Item"
