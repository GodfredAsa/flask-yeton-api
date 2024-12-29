from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from constants.app_constants import SQLALCHEMY_DATABASE_URI, DB_CONNECTION_STRING, SQL_MODIFICATION_STRING, \
    PROPAGATE_EXCEPTIONS, JWT_KEY, JWT_SECRET
from resource.TestServerResource import TestServerResource
from resource.AddressResource import AddressResource, GetUserAddressResource
from resource.CategoryResource import CategoriesResource, CategoryResource
from resource.FAQResouce import FAQsResource, FAQResource
from resource.ItemGalleryResource import GalleriesResource, ItemGalleryResource, GalleryResource
from resource.ItemResource import ItemsResource, ItemResource, AdminItemsResource, AdminItemResource
from resource.OrderItemResource import PlaceOrders, PlacedOrderResource, CancelPlacedOrder, AllUserOrders, \
    OrdersFulfilledResource
from resource.RegionsResource import RegionsResource, RegionResource
from resource.SummaryStatistics import SummaryStatisticsResource, OrderSummary, StockSummary, UserSummary
from resource.UserResource import UserRegistrationResource, UserLogin, LogoutUser, AdminUserResource, \
    BlackListUserResource
from db import db
from flask_cors import CORS

from resource.VendorResource import VendorResource, VendorItemResource, UnAssignItemVendorItemResource

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:4200"]}})
CORS(app)


jwt = JWTManager(app)
api = Api(app)

app.config[SQLALCHEMY_DATABASE_URI] = DB_CONNECTION_STRING
app.config[SQL_MODIFICATION_STRING] = False
app.config[PROPAGATE_EXCEPTIONS] = True
app.config[JWT_SECRET] = 'joe'


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

# ADMIN RESOURCES not used in postman BlackListUserResource
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

api.add_resource(TestServerResource, "/")


if __name__ == "__main__":
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)


#  sudo lsof -i :5000
# kill all processes on port 5002
# sudo lsof -t -i:5002 | xargs sudo kill -9
