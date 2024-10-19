from flask_restful import Resource
import http.client as status

from model.Item import ItemModel
from model.Vendor import VendorModel
from utils.GeneralUtils import return_message
from utils.UserUtils import validate_phone
from utils.VendorUtils import vendor_data


class VendorResource(Resource):
    def post(self):
        data = vendor_data()
        item = ItemModel.find_by_uuid(data['itemId'])
        if not validate_phone(data["phone"]):
            return return_message(status.BAD_REQUEST, "Invalid phone number")
        if not item:
            return return_message(status.BAD_REQUEST, "item not found")
        if VendorModel.find_by_phone(data['phone']):
            return return_message(status.BAD_REQUEST, f"vendor with {data['phone']} all exist")
        vendor = VendorModel(**data)
        vendor.save_to_db()
        return vendor.json()

    def get(self):
        return [vendor.json() for vendor in VendorModel.find_all()]


class VendorItemResource(Resource):
    def put(self, vendorId):
        data = vendor_data()
        item = ItemModel.find_by_uuid(data['itemId'])
        foundVendor = VendorModel.find_by_uuid(vendorId)
        if not foundVendor:
            return return_message(status.NOT_FOUND, "Vendor not found")

        if not validate_phone(data["phone"]):
            return return_message(status.BAD_REQUEST, "Invalid phone number")
        if not item:
            return return_message(status.BAD_REQUEST, "item not found")

        vendor = VendorModel(**data)
        vendor.save_to_db()
        return vendor.json()

    def get(self, vendorId):
        data = vendor_data()
        item = ItemModel.find_by_uuid(data['itemId'])
        vendor = VendorModel.find_by_uuid(vendorId)
        if not vendor:
            return return_message(status.NOT_FOUND, "Vendor not found")
        if not validate_phone(data["phone"]):
            return return_message(status.BAD_REQUEST, "Invalid phone number")
        if not item:
            return return_message(status.BAD_REQUEST, "item not found")

        vendor = VendorModel(**data)
        vendor.save_to_db()
        return vendor.json()

    def delete(self, vendorId):
        vendor = VendorModel.find_by_uuid(vendorId)
        if not vendor:
            return return_message(status.NOT_FOUND, "Vendor not found")
        vendor.delete_from_db()
        return return_message(status.OK, "Vendor deleted successfully"), status.OK
