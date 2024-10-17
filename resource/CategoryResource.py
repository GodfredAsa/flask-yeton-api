from flask_restful import Resource
import http.client as status
from model.Category import CategoryModel
from utils.CatgoryUtils import category_data
from utils.GeneralUtils import return_message


class CategoriesResource(Resource):
    def get(self):
        return [category.json() for category in CategoryModel.find_all_categories()], status.OK

    def post(self):
        data = category_data()
        if CategoryModel.find_by_category_name(data['name']):
            return return_message(400, "Category with the name already exists")
        category = CategoryModel(**data)
        category.save_to_db()
        return category.json(), status.CREATED


#  ALL ADMIN RESOURCES
class CategoryResource(Resource):
    def get(self, categoryId):
        category = CategoryModel.find_by_uuid(categoryId)
        if not category:
            return return_message(404, "Category not found"), status.NOT_FOUND
        return category.json(), status.OK

    def put(self, categoryId):
        data = category_data()
        category = CategoryModel.find_by_uuid(categoryId)
        if not category:
            return return_message(404, "Category not found"), status.NOT_FOUND
        category.name = data['name']
        category.categoryImageUrl = data['categoryImageUrl']
        category.save_to_db()
        return return_message(status.OK, "Category updated successfully"), status.OK

    def delete(self, categoryId):
        category = CategoryModel.find_by_uuid(categoryId)
        if not category:
            return return_message(404, "Category not found"), status.NOT_FOUND
        category.delete_from_db()
        return return_message(status.OK, "Category deleted successfully"), status.OK

