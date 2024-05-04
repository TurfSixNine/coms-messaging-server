
from flask_restful import Resource
class Status(Resource):
    def get():
        return {
            "status": "ok"
        }, 200