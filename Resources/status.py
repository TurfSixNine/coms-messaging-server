
from flask_restful import Resource
class Status(Resource):
    def get(self):
        return {
            "status": "ok"
        }, 200