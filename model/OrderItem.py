from datetime import datetime

from db import db
from typing import List

from enums.OrderStatus import OrderStatus
from enums.PaymentStatus import PaymentStatus
from model.User import UserModel
from model.Item import ItemModel
from utils.GeneralUtils import generate_uuid, generate_unique_code


class OrderItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    orderId = db.Column(db.String(10), unique=True)
    qty = db.Column(db.Integer, default=1)
    itemPrice = db.Column(db.Float, default=0.0)
    totalCost = db.Column(db.Float, default=0.0)
    userId: 'UserModel' = db.Column(db.String(10))
    itemId = db.Column(db.String(256))
    orderStatus = db.Column(db.String(256), default=OrderStatus.PENDING, nullable=False)
    paymentStatus = db.Column(db.String(256), default=PaymentStatus.PENDING, nullable=False)
    orderCode = db.Column(db.String(10), unique=True)
    createdAt = db.Column(db.String(256))
    updatedAt = db.Column(db.String(10))

    def __init__(self, qty, userId, itemId):
        self.qty = qty
        self.userId = userId
        self.itemId = itemId
        self.orderId = generate_uuid()
        self.itemPrice = ItemModel.find_by_uuid(itemId).sellingPrice
        self.totalCost = self.qty * self.itemPrice
        self.orderStatus = OrderStatus.PENDING
        self.paymentStatus = PaymentStatus.PENDING
        self.orderCode = generate_unique_code()
        self.createdAt = datetime.now().date()
        self.updatedAt = None

    def __str__(self):
        return f"< Order Items: Name:{ItemModel.find_by_uuid(self.itemId).name} " \
               f"Price:{ItemModel.find_by_uuid(self.itemId).sellingPrice} " \
               f"total Cost: {self.totalCost}"

    def json(self):
        return {
            "orderId": self.orderId,
            "price": self.itemPrice,
            "quantity": self.qty,
            "totalCost": self.totalCost,
            "item": self.itemId,
            "user": self.userId,
            "orderStatus": self.orderStatus,
            "paymentStatus": self.paymentStatus,
            "orderDate": str(self.createdAt),
            "updatedDate": str(self.updatedAt),
            "orderCode": self.orderCode
        }

    @classmethod
    def find_by_uuid(cls, orderId: str) -> 'OrderItemModel':
        return cls.query.filter_by(orderId=orderId).first()

    @classmethod
    def find_all_orders(cls) -> List['OrderItemModel']:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

