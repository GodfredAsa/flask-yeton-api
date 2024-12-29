import http.client as status

from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import Resource

from model.FAQ import FAQModel
from utils.FAQUtils import faq_data
from utils.GeneralUtils import return_message


class FAQsResource(Resource):
    def get(self):
        return [faq.json() for faq in FAQModel.find_all_faqs()], status.OK

    @jwt_refresh_token_required
    def post(self):
        data = faq_data()

        if FAQModel.find_by_title(data['title']):
            return return_message(status.CONFLICT, "FAQ with the title already exists")
        faq = FAQModel(**data)
        faq.save_to_db()
        return return_message(status.CREATED, "FAQ successfully added")


class FAQResource(Resource):
    @jwt_refresh_token_required
    def put(self, faqId):
        data = faq_data()
        faq = FAQModel.find_by_uuid(faqId)
        if not faq:
            return return_message(status.NOT_FOUND, "The FAQ not found")
        if data['title'] not in [f.title for f in FAQModel.find_all_faqs()]:
            faq.title = data['title']
            faq.message = data['message']
            faq.save_to_db()

            return return_message(status.OK, "FAQ successfully update")

        return return_message(status.CONFLICT, "The FAQ title already exists")

    def get(self, faqId):
        faq = FAQModel.find_by_uuid(faqId)
        if not faq:
            return return_message(status.NOT_FOUND, "The FAQ not found")
        return faq.json(), status.OK

    # @jwt_refresh_token_required
    def delete(self, faqId):
        faq = FAQModel.find_by_uuid(faqId)
        if not faq:
            return return_message(status.NOT_FOUND, "The FAQ not found")
        faq.delete_from_db()
        return return_message(status.OK, "FAQ deleted successfully"), status.OK
