from flask_restful import Resource
import http.client as status
from model.Item import ItemModel
from model.Vendor import VendorModel
from utils.GeneralUtils import return_message
from utils.UserUtils import validate_phone
from utils.VendorUtils import vendor_data, assign_item_vendor_data
from model.VendorItem import VendorItemModel


class VendorResource(Resource):
    def post(self):
        data = vendor_data()
        if not validate_phone(data["phone"]):
            return return_message(status.BAD_REQUEST, "Invalid phone number")
        if VendorModel.find_by_phone(data['phone']):
            return return_message(status.BAD_REQUEST, f"Vendor with {data['phone']} already exists")
        vendor = VendorModel(**data)
        vendor.save_to_db()
        return vendor.json()

    def get(self):
        return [vendor.json() for vendor in VendorModel.find_all()]


# ASSIGN ITEM TO VENDOR RESOURCE
class VendorItemResource(Resource):
    def put(self, vendorId):
        data = assign_item_vendor_data()

        if not VendorModel.find_by_uuid(vendorId):
            return return_message(status.NOT_FOUND, "Vendor not found")
        if not ItemModel.find_by_uuid(data['itemId']):
            return return_message(status.BAD_REQUEST, "item not found")
        if VendorItemModel.find_by_item_uuid(data['itemId']).vendorId == vendorId:
            return return_message(status.BAD_REQUEST, "Item Already assigned to Vendor")
        vendorItem = VendorItemModel(itemId=data['itemid'], vendorId=vendorId)
        vendorItem.save_to_db()
        return VendorModel.find_by_uuid(vendorId).json(), status.OK

    def get(self, vendorId):
        vendor = VendorModel.find_by_uuid(vendorId)
        if not vendor:
            return return_message(status.NOT_FOUND, "Vendor not found")
        return vendor.json()

    def delete(self, vendorId):
        vendor = VendorModel.find_by_uuid(vendorId)
        if not vendor:
            return return_message(status.NOT_FOUND, "Vendor not found")
        vendor.delete_from_db()
        return return_message(status.OK, "Vendor deleted successfully"), status.OK


class UnAssignItemVendorItemResource(Resource):
    def put(self, vendorId, itemId):
        vendor = VendorModel.find_by_uuid(vendorId)
        item = ItemModel.find_by_uuid(itemId)
        if not vendor:
            return return_message(status.NOT_FOUND, "Vendor not found")
        if not item:
            return return_message(status.NOT_FOUND, "Item not found")
        vendorItem = VendorItemModel.find_by_item_uuid(itemId)
        if not vendorItem:
            return return_message(status.NOT_FOUND, "Vendor do not have this item assigned")
        vendorItem.delete_from_db()
        return return_message(status.OK, "Item unassigned to vendor"), status.OK

