from flask_restful import Resource
from util import Util, token_required

class Insights(Resource, Util):
    def __init__(self):
        pass
    @token_required
    def get(self,type):
        if type == "SMS":
            return self.get_messaging_insights()
        else:
                return self.get_calls_insights()        

    def post(self):
        pass
    
