from datetime import datetime

from db import db
from model.Category import CategoryModel
from model.Gallery import GalleryModel
from utils.GeneralUtils import generate_uuid, generate_unique_code, str_to_bool


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(20), unique=True)
    categoryId = db.Column(db.String(20))
    name = db.Column(db.String(80), nullable=False)
    brand = db.Column(db.String(250))
    condition = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    sellingPrice = db.Column(db.Float, default=0.0, nullable=False)
    cost = db.Column(db.Float, default=0.0, nullable=False)
    stock = db.Column(db.Integer, default=1)
    image = db.Column(db.String(256), nullable=False)
    galleryId = db.Column(db.String(256), nullable=True)
    hasGallery = db.Column(db.Boolean, default=True, nullable=False)
    itemCode = db.Column(db.String(256), nullable=True)
    forSale = db.Column(db.Boolean, default=True)
    profit = db.Column(db.Float, default=0.0, nullable=False)
    createdAt = db.Column(db.String(256))
    updatedAt = db.Column(db.String(10))

    def __init__(self, categoryId, name, brand, condition, model, price, stock, image, hasGallery, forSale, cost):
        self.categoryId = categoryId
        self.name = name
        self.brand = brand
        self.condition = condition
        self.model = model
        self.sellingPrice = price
        self.cost = cost
        self.stock = stock
        self.image = image
        self.forSale = str_to_bool(forSale)
        self.hasGallery = str_to_bool(hasGallery)
        self.item_id = generate_uuid()
        self.itemCode = generate_unique_code()
        self.createdAt = datetime.now()
        self.profit = self.stock * (self.sellingPrice - self.cost)

    def adminJson(self):
        return {
            "itemId": self.item_id,
            "itemName": self.name,
            "category": CategoryModel.find_by_uuid(self.categoryId).json() if self.hasGallery else None,
            "brand": self.brand,
            "condition": self.condition,
            "model": self.model,
            "stock": self.stock,
            "image": self.image,
            "price": self.sellingPrice,
            "cost": self.cost,
            "hasGallery": self.hasGallery,
            "profit": self.profit,
            "forSale": self.forSale,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

    def json(self):
        return {
            "itemId": self.item_id,
            "name": self.name,
            "category": CategoryModel.find_by_uuid(self.categoryId).json(),
            "brand": self.brand,
            "condition": self.condition,
            # "gallery": GalleryModel.find_by_uuid(self.galleryId).json(),
            "model": self.model,
            "stock": self.stock,
            "image": self.image,
            "price": self.sellingPrice,
        }

    @classmethod
    def find_by_uuid(cls, itemId: str) -> 'ItemModel':
        return cls.query.filter_by(item_id=itemId).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
