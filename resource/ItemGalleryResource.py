from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import Resource

from model.Gallery import GalleryModel
from model.Item import ItemModel
from utils.GalleryUtils import gallery_data
from utils.GeneralUtils import return_message
import http.client as status


class GalleriesResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        data = gallery_data()
        item = ItemModel.find_by_uuid(data['itemId'])
        if not item:
            return return_message(404, "Item not found")
        if not item.hasGallery:
            return return_message(419, "Item cannot have galleries")
        gallery = GalleryModel(**data)
        gallery.save_to_db()
        return gallery.json()

    def get(self):
        return [gallery.json() for gallery in GalleryModel.find_all()]


class ItemGalleryResource(Resource):
    def get(self, itemId):
        return [gallery.json() for gallery in GalleryModel.find_all() if gallery.itemId == itemId]


class GalleryResource(Resource):
    def get(self, galleryId):
        gallery = GalleryModel.find_by_uuid(galleryId)
        if not gallery:
            return return_message(status.NOT_FOUND, "Gallery not found"), status.NOT_FOUND
        return gallery.json(), status.OK

    @jwt_refresh_token_required
    def put(self, galleryId):
        data = gallery_data()
        gallery = GalleryModel.find_by_uuid(galleryId)
        if not gallery:
            return return_message(status.NOT_FOUND, "Gallery not found"), status.NOT_FOUND
        gallery.itemId = data['itemId']
        gallery.image = data['image']
        gallery.save_to_db()
        return return_message(status.OK, "Gallery updated successfully"), status.OK

    @jwt_refresh_token_required
    def delete(self, galleryId):
        gallery = GalleryModel.find_by_uuid(galleryId)
        if not gallery:
            return return_message(status.NOT_FOUND, "Gallery not found"), status.NOT_FOUND
        gallery.delete_from_db()
        return return_message(status.OK, "Gallery deleted successfully"), status.OK



