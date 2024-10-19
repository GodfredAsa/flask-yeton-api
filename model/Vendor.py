from datetime import datetime

from db import db
from model.Item import ItemModel
from typing import List
from utils.GeneralUtils import generate_uuid


class VendorModel(db.Model):
    __tablename__ = "vendors"
    id = db.Column(db.Integer, primary_key=True)
    vendorId = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    itemId = db.Column(db.String(10), nullable=False, unique=True)
    createdAt = db.Column(db.String(250))

    def __init__(self, name, phone, itemId):
        self.name = name
        self.phone = phone
        self.itemId = itemId
        self.vendorId = generate_uuid()
        self.createdAt = datetime.now()

    def json(self):
        return {
            "vendorId": self.vendorId,
            "name": self.name,
            "phone": self.phone,
            "createdAt": str(self.createdAt),
            "item": [ItemModel.find_by_uuid(self.itemId).adminJson()]
        }

    @classmethod
    def find_by_phone(cls, phone: str) -> 'VendorModel':
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_uuid(cls, vendorId: str) -> 'VendorModel':
        return cls.query.filter_by(vendorId=vendorId).first()

    @classmethod
    def find_all(cls) -> List['VendorModel']:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

