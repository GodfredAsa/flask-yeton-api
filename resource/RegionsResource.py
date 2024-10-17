from flask_jwt_extended import jwt_refresh_token_required

from model.Region import RegionModel
from utils.RegionUtils import region_data, region_exists_by_name
from flask_restful import Resource
import http.client as status
from utils.GeneralUtils import return_message


class RegionsResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        data = region_data()
        if region_exists_by_name(data["name"]):
            return return_message(status.BAD_REQUEST, f"{data['name']} region already exists"), status.BAD_REQUEST
        region = RegionModel(**data)
        region.save_to_db()
        return region.json(), status.CREATED

    def get(self):
        return [region.json() for region in RegionModel.find_all_regions()]


class RegionResource(Resource):
    def get(self, id: str):
        region = RegionModel.find_by_uuid(id)
        if not RegionModel.find_by_uuid(id):
            return return_message(404, "Region not Found"), 404
        return region.json(), 200

    @jwt_refresh_token_required
    def delete(self, id: str):
        region = RegionModel.find_by_uuid(id)
        if not RegionModel.find_by_uuid(id):
            return return_message(404, "Region not Found"), 404
        region.delete_from_db()
        return return_message(200, "Region deleted successfully"), 200




