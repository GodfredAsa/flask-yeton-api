from db import db
from utils.GeneralUtils import generate_uuid

from typing import List


class GalleryModel(db.Model):
    __tablename__ = "galleries"
    id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.String(20), unique=True)
    itemId = db.Column(db.String(256), nullable=False)
    image = db.Column(db.String(256))

    def __init__(self, itemId, image):
        self.galleryId = generate_uuid()
        self.image = image
        self.itemId = itemId
        self.gallery_id = generate_uuid()

    def json(self):
        return {
            "galleryId": self.gallery_id,
            "itemId": self.itemId,
            "image": self.image
        }

    @classmethod
    def find_by_uuid(cls, galleryId: str) -> 'GalleryModel':
        return cls.query.filter_by(gallery_id=galleryId).first()

    @classmethod
    def find_all(cls) -> List['GalleryModel']:
        return cls.query.all()

    @classmethod
    def find_gallery_by_item_id(cls, itemId: str) -> List['GalleryModel']:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
