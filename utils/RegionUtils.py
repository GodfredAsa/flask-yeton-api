from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR
from model.Region import RegionModel

_region_parser = reqparse.RequestParser()
_region_parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))
_region_parser.add_argument("city", type=str, required=True, help=BLANK_ERROR.format("city"))



def region_data():
    return _region_parser.parse_args()


def region_exists_by_name(name: str):
    return False if not RegionModel.find_region_by_name(name) else True

