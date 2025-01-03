from db import db
from utils.GeneralUtils import generate_uuid
from  typing import List


class VendorItemModel(db.Model):
    __tablename__ = "vendor_items"
    id = db.Column(db.Integer, primary_key=True)
    vendorItemId = db.Column(db.String(20), unique=True)
    itemId = db.Column(db.String(80), unique=True)
    vendorId = db.Column(db.String(250))

    def __init__(self, itemId, vendorId):
        self.itemId = itemId
        self.vendorId = vendorId
        self.vendorItemId = generate_uuid()

    @classmethod
    def find_by_uuid(cls, vendorItemId: str) -> 'VendorItemModel':
        return cls.query.filter_by(vendorItemId=vendorItemId).first()

    @classmethod
    def find_by_item_uuid(cls, itemId: str) -> 'VendorItemModel':
        return cls.query.filter_by(itemId=itemId).first()

    @classmethod
    def find_all(cls) -> List['VendorItemModel']:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()