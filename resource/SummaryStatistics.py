from flask_restful import Resource

from enums.OrderStatus import OrderStatus
from model.Category import CategoryModel
from model.Item import ItemModel
from model.OrderItem import OrderItemModel
from model.User import UserModel
from functools import reduce
from operator import add
from collections import defaultdict

class SummaryStatisticsResource(Resource):
    def get(self):
        onlineUsers, offlineUsers, totalProfit, totalRevenue, numberOfPendingOrders, numberOfFulfilledOrders, numberOfCategories = 0, 0, 0, 0, 0, 0, 0
        for user in UserModel.find_all_users():
            onlineUsers, offlineUsers = (onlineUsers + 1, offlineUsers) if user.isOnline else (
            onlineUsers, offlineUsers + 1)
            totalProfit = [item.profit for item in ItemModel.find_all()]
            totalRevenue = [item.cost * item.stock for item in ItemModel.find_all()]
            numberOfPendingOrders = len(
                [order for order in OrderItemModel.find_all_orders() if order.orderStatus == OrderStatus.PENDING]),
            numberOfFulfilledOrders = len(
                [order for order in OrderItemModel.find_all_orders() if order.orderStatus == OrderStatus.COMPLETED]),
            numberOfCategories = 0 if len(CategoryModel.find_all_categories()) <= 0 else len(
                CategoryModel.find_all_categories())
        return {
            'userStats': {'online': onlineUsers, 'offline': offlineUsers, 'totalUsers': onlineUsers + offlineUsers},
            'orderSummary': {
                'pending': numberOfPendingOrders[0],
                'completedOrders': numberOfFulfilledOrders[0]
            },
            'currentStock': reduce(add, [item.stock for item in ItemModel.find_all()], 0),
            'expectedProfit': sum(totalProfit),
            'totalRevenue': sum(totalRevenue),
            'categories': numberOfCategories
        }


class OrderSummary(Resource):

    def get(self):
        expectedProfit = sum([order.totalProfit for order in OrderItemModel.find_all_orders()])
        earnedProfit = sum([order.totalProfit for order in OrderItemModel.find_all_orders() if
                            order.orderStatus == OrderStatus.COMPLETED])
        return {
            "pendingOrders": len(
                [order for order in OrderItemModel.find_all_orders() if order.orderStatus == OrderStatus.PENDING]),
            "costOfSoldItems": sum([order.totalCost for order in OrderItemModel.find_all_orders()]),
            "expectedProfit": expectedProfit - earnedProfit,
            "earnedProfit": earnedProfit
        }


class StockSummary(Resource):

    def get(self):
        return {
            "totalStock": sum([stock.stock for stock in ItemModel.find_all()]),
            "stockWorth": sum([stock.stock * stock.sellingPrice for stock in ItemModel.find_all()]),
            "stockProfit": sum([stock.profit for stock in ItemModel.find_all()]),
        }


class UserSummary(Resource):

    def get(self):
        return {
            "totalUsers": len([user for user in UserModel.find_all_users()]),
            "blocked": len([user for user in UserModel.find_all_users() if user.isBlackListed]),
            "admins": len([user for user in UserModel.find_all_users() if user.is_admin]),
            "customers": len([user for user in UserModel.find_all_users() if not user.is_admin]),
        }


class VendorItemAndItems(Resource):

    def get(self):
        vendorItems = len([item for item in ItemModel.find_all() if item.hasVendor])
        nonVendorItems = len([item for item in ItemModel.find_all() if not item.hasVendor])
        return {
            "data": [vendorItems, nonVendorItems],
            "labels": ["Vendor", "None Vendor"]
        }


class StockLevelSummary(Resource):

    def get(self):
        return {
            "data": [item.stock for item in ItemModel.find_all()],
            "labels": [item.name for item in ItemModel.find_all()],
        }


class DailySalesSummary(Resource):
    def get(self):
        sales = []
        retData = []
        labels = []
        profits = []
        data = OrderItemModel.find_all_orders()
        sales_per_day = defaultdict(float)
        for order in data:
            order_date = order.createdAt
            total_cost = order.totalCost

            labels.append(order_date)
            retData.append(total_cost)
            profits.append(order.totalProfit)

            sales.append(sales_per_day)

        return {
            "data": retData,
            "labels": labels,
            "profits": profits
        }