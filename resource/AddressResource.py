from flask_restful import Resource
import http.client as status
from model.Address import AddressModel
from model.Region import RegionModel
from model.User import UserModel

from utils.AddressUtils import get_address_data
from utils.GeneralUtils import return_message


class AddressResource(Resource):
    def post(self):
        data = get_address_data()
        if not RegionModel.find_by_uuid(data['regionId']):
            return return_message(status.NOT_FOUND, "Region not found"), status.NOT_FOUND

        user = UserModel.find_by_uuid(data['userId'])
        if not user:
            return return_message(status.NOT_FOUND, "User not found "), status.NOT_FOUND

        f_address = AddressModel.find_address_by_userId(data["userId"])

        if f_address:
            f_address.regionId = data["regionId"]
            f_address.location = data["location"]
            f_address.save_to_db()
            return return_message(status.OK, "Address updated successfully")

        address = AddressModel(**data)
        address.save_to_db()
        return return_message(status.CREATED, "Address added successfully"), status.CREATED

    def get(self):
        return [address.json() for address in AddressModel.find_all_addresses()]


class GetUserAddressResource(Resource):

    def get(self, userId: str):
        if not UserModel.find_by_uuid(userId):
            return return_message(status.NOT_FOUND, "User address not found"), status.NOT_FOUND
        return AddressModel.find_address_by_userId(userId).json(), status.OK
