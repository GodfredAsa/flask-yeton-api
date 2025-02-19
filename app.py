from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_restful import Resource
from flask import Flask, request, jsonify
from datetime import datetime
import json
from flask_socketio import SocketIO, emit, disconnect
from constants.app_constants import SQLALCHEMY_DATABASE_URI, DB_CONNECTION_STRING, SQL_MODIFICATION_STRING, \
    PROPAGATE_EXCEPTIONS, JWT_KEY, JWT_SECRET
from resource.TestServerResource import TestServerResource
from resource.AddressResource import AddressResource, GetUserAddressResource
from resource.CategoryResource import CategoriesResource, CategoryResource
from resource.FAQResouce import FAQsResource, FAQResource
from resource.ItemGalleryResource import GalleriesResource, ItemGalleryResource, GalleryResource
from resource.ItemResource import ItemsResource, ItemResource, AdminItemsResource, AdminItemResource
from resource.OrderItemResource import PlaceOrders, PlacedOrderResource, CancelPlacedOrder, AllUserOrders, \
    OrdersFulfilledResource, AllOrders
from resource.RegionsResource import RegionsResource, RegionResource
from resource.SummaryStatistics import SummaryStatisticsResource, OrderSummary, StockSummary, UserSummary, \
    VendorItemAndItems, StockLevelSummary, DailySalesSummary
from resource.UserResource import UserRegistrationResource, UserLogin, LogoutUser, AdminUserResource, \
    BlackListUserResource
from db import db
from flask_cors import CORS

from resource.VendorResource import VendorResource, VendorItemResource, UnAssignItemVendorItemResource
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:4200"]}})
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:4200")

jwt = JWTManager(app)
api = Api(app)

app.config[SQLALCHEMY_DATABASE_URI] = DB_CONNECTION_STRING
app.config[SQL_MODIFICATION_STRING] = False
app.config[PROPAGATE_EXCEPTIONS] = True
app.config[JWT_SECRET] = 'joe'
# socketio = SocketIO(app, cors_allowed_origins="http://localhost:4200")

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegistrationResource, "/api/register")
api.add_resource(UserLogin, "/api/login")
api.add_resource(LogoutUser, "/api/users/logout")

api.add_resource(RegionsResource, "/api/regions")
api.add_resource(RegionResource, "/api/regions/<string:id>")

api.add_resource(AddressResource, "/api/address")
api.add_resource(GetUserAddressResource, "/api/addresses/users/<string:userId>")

api.add_resource(FAQsResource, "/api/faqs")
api.add_resource(FAQResource, "/api/faqs/<string:faqId>")

api.add_resource(CategoriesResource, "/api/categories")
api.add_resource(CategoryResource, "/api/categories/<string:categoryId>")

api.add_resource(ItemsResource, "/api/items")
api.add_resource(ItemResource, "/api/items/<string:itemId>")

api.add_resource(GalleriesResource, "/api/galleries")
api.add_resource(GalleryResource, "/api/galleries/<string:galleryId>")
api.add_resource(ItemGalleryResource, "/api/galleries/items/<string:itemId>")

api.add_resource(PlaceOrders, "/api/placed-orders")
api.add_resource(PlacedOrderResource, "/api/placed-orders/<string:orderId>")
api.add_resource(CancelPlacedOrder, "/api/orders/<string:orderId>/cancel")
api.add_resource(AllUserOrders, "/api/users/<string:userId>/orders")  # user orders

api.add_resource(OrdersFulfilledResource, "/api/admin/orders/fulfilled")  # user orders
api.add_resource(AllOrders, "/api/orders/users/<string:phone>")  # user orders

# ADMIN RESOURCES not used an BlackListUserResource
api.add_resource(AdminUserResource, "/api/users/admin")
api.add_resource(AdminItemsResource, "/api/admin/items")
api.add_resource(AdminItemResource, "/api/admin/items/<string:itemId>")
api.add_resource(BlackListUserResource, "/api/admin/users/<string:phone>/blacklist")
api.add_resource(VendorResource, "/api/vendors")
api.add_resource(VendorItemResource, "/api/vendors/<string:vendorId>")
api.add_resource(UnAssignItemVendorItemResource, "/api/vendors/<string:vendorId>/<string:itemId>/un-assign")

# DASHBOARD STATISTICS
api.add_resource(SummaryStatisticsResource, "/api/summary")
api.add_resource(OrderSummary, "/api/admin/order-summary")
api.add_resource(StockSummary, "/api/admin/stock-summary")
api.add_resource(UserSummary, "/api/admin/user-summary")
api.add_resource(VendorItemAndItems, "/api/admin/vendor-item")
api.add_resource(StockLevelSummary, "/api/admin/stock-levels")
api.add_resource(DailySalesSummary, "/api/admin/daily-sales")

api.add_resource(TestServerResource, "/")

connected_clients = {}


@app.route('/api/connect', methods=['POST'])
def connect_client():
    data = request.get_json()
    client_id = data.get('clientId')
    if not client_id:
        return jsonify({'error': 'Client ID is required'}), 400

    if client_id not in connected_clients:
        connected_clients[client_id] = {
            'id': client_id,
            'connected_at': datetime.now().isoformat(),
            'ip_address': request.remote_addr
        }
        socketio.emit('client_connected', connected_clients[client_id])

    return jsonify(connected_clients[client_id]), 200


@app.route('/api/disconnect', methods=['POST'])
def disconnect_client():
    data = request.get_json()
    client_id = data.get('clientId')
    if not client_id:
        return jsonify({'error': 'Client ID is required'}), 400

    if client_id in connected_clients:
        client_info = connected_clients.pop(client_id)
        socketio.emit('client_disconnected', {
            'client_id': client_id,
            'disconnected_at': datetime.now().isoformat()
        })
        return jsonify({'status': 'disconnected', 'client_info': client_info}), 200

    return jsonify({'error': 'Client not found'}), 404


@app.route('/api/clients', methods=['GET'])
def get_connected_clients():
    return jsonify({
        'connected_clients': len(connected_clients),
        'clients': list(connected_clients.values())
    })


@app.route('/api/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'message' not in data or 'clientId' not in data:
        return jsonify({'error': 'Message and clientId are required'}), 400

    message_data = {
        'client_id': data['clientId'],
        'message': data['message'],
        'timestamp': datetime.now().isoformat()
    }
    socketio.emit('message', message_data)
    return jsonify({'status': 'Message sent', 'message': message_data}), 200


# WebSocket event handlers
@socketio.on_error()
def error_handler(e):
    print(f"Error: {e}")
    emit('error', {'error': str(e)})

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5001, debug=True)


#  sudo lsof -i :5000
# kill all processes on port 5002
# sudo lsof -t -i:5002 | xargs sudo kill -9
