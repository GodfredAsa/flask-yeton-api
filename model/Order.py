#
# from enum import Enum
# from datetime import datetime
# from db import db
# from enums.OrderStatus import OrderStatus
# from enums.PaymentStatus import PaymentStatus
# from utils.GeneralUtils import generate_unique_code
#
# # I NEED ORDER ITEM TABLE AS WELL.
#
#
# class OrderModel(db.Model):
#     __tablename__ = 'orders'
#     id = db.Column(db.Integer, unique=True)
#     orderId = db.Column(db.String(10), unique=True)
#     orderCode = db.Column(db.String(10), unique=True)
#
#     totalCost = db.Column(db.Float, default=0.0)
#     orderStatus = db.Column(db.Enum(OrderStatus), unique=OrderStatus.PENDING, nullable=False)  # PENDING, DELIVERED, COMPLETED
#     paymentStatus = db.Column(Enum(PaymentStatus), unique=PaymentStatus.PENDING, nullable=False)
#     createdAt = db.Column(db.String(256))
#     updatedAt = db.Column(db.String(10))
#
#     def __init__(self):
#         self.totalCost = 0.0
#         self.orderStatus = OrderStatus.PENDING
#         self.paymentStatus = PaymentStatus.PENDING
#         self.orderCode = generate_unique_code()
#         self.createdAt = datetime.now().date()
#         self.updatedAt = None
#
#     def __str__(self):
#         pass
#
#     def json(self):
#         return {
#             "orderId": self.orderId,
#             "orderCode": self.orderCode,
#             "totalCost": self.totalCost,
#             "orderStatus": self.orderStatus,
#             "paymentStatus": self.paymentStatus,
#             "createdAt": self.createdAt,
#             "updatedAt": self.updatedAt
#         }
#
#     @classmethod
#     def find_by_uuid(cls, orderId: str) -> 'OrderModel':
#         return cls.query.filter_by(orderId=orderId).first()
#
#     @classmethod
#     def find_all_orders(cls):
#         return cls.query.all()
#
#     def save_to_db(self) -> None:
#         db.session.add(self)
#         db.session.commit()
#
#     def delete_from_db(self) -> None:
#         db.session.delete(self)
#         db.session.commit()
