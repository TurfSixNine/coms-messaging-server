from flask_restful import Resource, request
from services.db import mongo
import os
from bson.objectid import ObjectId
from bson import json_util
from util import Util, token_required
import os
import json

class Group(Resource, Util):
    def __init__(self ):        
        self.user_collection  = mongo.db.users
        self.group_collection  = mongo.db.groups
    @token_required    
    def get(self, user):
        try:
            return self.get_user_groups(user), 200
        except Exception as e:
            print(str(e))
            return str(e), 500
    @token_required    
    def post(self, user):
        try:
            # get params from user token
            form = request.get_json(force=True)
            response = []
            # store new group
            self.group_collection.insert_one(
                {"user_id": ObjectId(user['id']), 
                'name': form['name'],
                'numbers': form['numbers']   
                })    
            # gets all groups created by user
            response = self.get_user_groups(user)
            return response, 201
        except Exception as e:
            print(str(e))
            return {"error": str(e)}, 500
    @token_required    
    def delete(self, id, user):
        try:
            deleted_group = dict(self.group_collection.find_one_and_delete({'_id': ObjectId(id)}))
            self.to_valid_dict_response(deleted_group)
            return self.get(user=user)
        except Exception as e:
            print(str(e))
            return str(e), 500
    def get_user_groups(self, user):
        response = []
        groups = []
        if user['role'] == os.environ['ADMIN']: 
            groups = self.group_collection.find({})         
        else:
            groups = self.group_collection.find({'user_id': ObjectId(user['id'])})        
        for group in groups:
            group['_id'] = str(group['_id'])
            # del group['_id']
            del group['user_id'] 
            response.append(self.to_valid_dict_response({**group}))
        return response