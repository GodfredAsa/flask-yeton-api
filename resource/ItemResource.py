from datetime import datetime
import http.client as status

from flask import jsonify
from flask_jwt import jwt_required
from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import Resource
from model.Category import CategoryModel
from model.Gallery import GalleryModel
from model.Item import ItemModel
from utils.GeneralUtils import return_message, str_to_bool
from utils.ItemUtils import item_data


#  SEPARATE RESOURCE INTO ADMIN AND USER LOOK INTO THE ITEM RESOURCE AND WORK ON IT EXTENSIBLE


class ItemsResource(Resource):

    def get(self):
        return [item.json() for item in ItemModel.find_all() if item.forSale]


class ItemResource(Resource):
    def get(self, itemId):
        item = ItemModel.find_by_uuid(itemId)
        if not item:
            return return_message(status.NOT_FOUND, "Item not found"), status.NOT_FOUND
        return item.json(), status.OK

# ADMIN RESOURCES


class AdminItemsResource(Resource):

    @jwt_refresh_token_required
    def post(self):
        data = item_data()
        if not CategoryModel.find_by_uuid(data['categoryId']):
            return return_message(404, "Category not found")
        if data['condition'] not in ["NEW", "SLIGHTLY USED"]:
            return return_message(400, "Condition should be NEW or SLIGHTLY USED")
        item = ItemModel(**data)
        item.save_to_db()
        return jsonify(item.adminJson())

    def get(self):
        return [item.adminJson() for item in ItemModel.find_all()]


class AdminItemResource(Resource):
    @jwt_refresh_token_required
    def put(self, itemId):
        data = item_data()
        item = ItemModel.find_by_uuid(itemId)
        if not item:
            return return_message(status.NOT_FOUND, "Item not found"), status.NOT_FOUND

        item.name = data['name']
        item.categoryId = data['categoryId']
        item.brand = data['brand']
        item.condition = data['condition']
        item.model = data['model']
        item.price = data['price']
        item.stock = data['stock']
        item.profit = data['stock'] * (data['price'] - data['cost'])
        item.image = data['image']
        item.forSale = str_to_bool(data['forSale'])

        if not data['hasGallery']:
            galleries = GalleryModel.find_gallery_by_item_id(itemId)
            for gallery in galleries:
                gallery.delete_from_db()

        item.hasGallery = data['hasGallery']
        item.updatedAt = datetime.now()
        item.save_to_db()
        return return_message(status.OK, "Item updated successfully ")

    def get(self, itemId):
        item = ItemModel.find_by_uuid(itemId)
        if not item:
            return return_message(status.NOT_FOUND, "Item not found"), status.NOT_FOUND
        return item.adminJson(), status.OK

    @jwt_refresh_token_required
    def delete(self, itemId):
        item = ItemModel.find_by_uuid(itemId)
        if not item:
            return return_message(status.NOT_FOUND, "Item not found"), status.NOT_FOUND
        item.delete_from_db()
        return return_message(status.OK, "Item Deleted Successfully"), status.OK

