from flask_restful import Resource


class TestServerResource(Resource):
    def get(self):
        return {
            "status": 200,
            "message": "Working"
        }