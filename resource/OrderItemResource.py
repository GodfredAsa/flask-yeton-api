from datetime import datetime

from flask_jwt import jwt_required
from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import Resource

from enums.OrderStatus import OrderStatus
from enums.PaymentStatus import PaymentStatus
from model.Item import ItemModel
from model.OrderItem import OrderItemModel
from model.User import UserModel
from utils.GeneralUtils import return_message
from utils.OrderItemUtils import order_data
import http.client as status


class PlaceOrders(Resource):
    def get(self):  # NOT COMPLETED ORDERS
        return [order.json() for order in OrderItemModel.find_all_orders() if order.orderStatus != OrderStatus.COMPLETED]

    # @jwt_required
    def post(self):
        data = order_data()
        user = UserModel.find_by_uuid(data['userId'])
        item = ItemModel.find_by_uuid(data['itemId'])

        if not user:
            return return_message(status.NOT_FOUND, "User not found")
        if not item:
            return return_message(status.NOT_FOUND, "Item not found")

        if item.stock <= 0:
            return return_message(status.BAD_REQUEST, "Item out of stock"), status.BAD_REQUEST

        if data['qty'] <= 0:
            return return_message(status.BAD_REQUEST, f"Sorry you cannot purchase {data['qty']} of {item.name}"), status.BAD_REQUEST

        if data['qty'] > item.stock:
            return return_message(status.CONFLICT, f"Sorry the requested item available stock is {item.stock}")

        item.stock -= data['qty']
        item.save_to_db()
        orderItem = OrderItemModel(data['qty'], user.user_id, item.item_id)
        orderItem.save_to_db()

        return orderItem.json()


class PlacedOrderResource(Resource):
    @jwt_required
    def get(self, orderId):
        order = OrderItemModel.find_by_uuid(orderId)
        if not order:
            return return_message(status.NOT_FOUND, "Order not found")
        return order.json()

    # WILL NOT PERMIT THE DELETION OF AN ITEM. PATRICK DECIDE
    @jwt_refresh_token_required
    @jwt_required
    def delete(self, orderId):
        order = OrderItemModel.find_by_uuid(orderId)
        if not order:
            return return_message(status.NOT_FOUND, "Order not found"), status.NOT_FOUND
        if order.orderStatus == OrderStatus.COMPLETED or order.orderStatus == OrderStatus.CANCELLED:
            return return_message(status.BAD_REQUEST, "You cannot delete a cancelled or fulfilled order"), status.BAD_REQUEST
        item = ItemModel.find_by_uuid(order.itemId)
        item.stock += order.qty
        item.save_to_db()
        order.delete_from_db()
        return return_message(status.OK, "Order deleted successfully"), status.OK

    # FULFILLING AN ORDER OR COMPLETE THE ORDER
    @jwt_refresh_token_required
    def put(self, orderId):
        order = OrderItemModel.find_by_uuid(orderId)
        if not order:
            return return_message(status.NOT_FOUND, "Order not found")
        if order.orderStatus == OrderStatus.COMPLETED:
            return return_message(status.BAD_REQUEST, f"Order with code {order.orderCode} already fulfilled")
        order.orderStatus = OrderStatus.COMPLETED
        order.paymentStatus = PaymentStatus.PAID
        order.updatedAt = str(datetime.now())
        order.save_to_db()
        return return_message(status.OK, f"Order with code {order.orderCode} fulfilled")


class CancelPlacedOrder(Resource):
    @jwt_refresh_token_required
    @jwt_required
    def put(self, orderId):
        order = OrderItemModel.find_by_uuid(orderId)
        if not order:
            return return_message(status.NOT_FOUND, "Order not found"), status.NOT_FOUND
        if order.orderStatus == OrderStatus.COMPLETED:
            return return_message(status.BAD_REQUEST, "Completed Order cannot be cancelled"), status.BAD_REQUEST
        if order.orderStatus == OrderStatus.CANCELLED:
            return return_message(status.CONFLICT, "Order is already cancelled"), status.CONFLICT
        item = ItemModel.find_by_uuid(order.itemId)
        item.stock += order.qty
        item.save_to_db()
        order.delete_from_db()
        return return_message(status.OK, f"Order with {order.orderCode} code cancelled successfully")


class OrdersFulfilledResource(Resource):
    @jwt_refresh_token_required
    def get(self):
        return [order.json() for order in OrderItemModel.find_all_orders() if order.orderStatus == OrderStatus.COMPLETED]


class AllUserOrders(Resource):
    @jwt_refresh_token_required
    @jwt_required
    def get(self, userId):
        return [order.json() for order in OrderItemModel.find_all_orders() if order.userId == userId and order.orderStatus == OrderStatus.PENDING]
