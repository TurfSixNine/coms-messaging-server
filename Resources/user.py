from flask_restful import Resource
from services.db import mongo
from util import token_required
import os
from bson.objectid import ObjectId
 

class User(Resource):
    def __init__(self):
        self.user_collection  = mongo.db.users
    @token_required
    def get(self,user):
        try:
            response = []
            users = []
            if user['role'] == os.environ['ADMIN']:
                users = self.user_collection.find({})
            else:
                users = self.user_collection.find({'id': ObjectId([id])})    
            for user in users:
                user['id'] = str(user['_id'])
                # del group['_id']
                del user['_id'] 
                del user['password'] 
                response.append(user)
            return response
        except Exception as e:
            print(str(e))
            return str(e), 500          
 