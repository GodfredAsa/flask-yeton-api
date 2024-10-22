from datetime import datetime

from flask import jsonify

from db import db
from model.Item import ItemModel
from typing import List

from model.VendorItem import VendorItemModel
from utils.GeneralUtils import generate_uuid


class VendorModel(db.Model):
    __tablename__ = "vendors"
    id = db.Column(db.Integer, primary_key=True)
    vendorId = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    createdAt = db.Column(db.String(250))

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.vendorId = generate_uuid()
        self.createdAt = datetime.now()

    def json(self):
        vendors_items = []

        for vi in VendorItemModel.find_all():
            if vi.vendorId == self.vendorId:
                vendors_items.append(vi.itemId)
        return {
            "vendorId": self.vendorId,
            "name": self.name,
            "phone": self.phone,
            "createdAt": str(self.createdAt),
            "item": [ItemModel.find_by_uuid(ID).json() for ID in vendors_items]
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

