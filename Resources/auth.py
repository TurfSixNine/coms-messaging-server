from flask_restful import Resource, request
from services.db import mongo
import bcrypt
from util import Util
import os

class Auth(Resource, Util):
    def __init__ (self):
        self.user_collection  = mongo.db.users
    def post(self, route):
        form = request.get_json(force=True)

        if route == "sign-up":
            return self.sign_up(form)
        else:
            return self.sign_in(form)
    def sign_up(self, form):
        try:
            hashed_password = bcrypt.hashpw(bytes(form['password'], 'utf-8'), bcrypt.gensalt(12))
            data = {
                'username' : form['username'],
                'password': hashed_password,
                'email':form['email'],
                'role':os.environ['BASIC_USER'],
                
            }
            user = self.user_collection.insert_one(data)
            jwt_token = self.create_jwt({**data, 'id': str(user.inserted_id)})
            
            del data['role']
            del data['password']
            return {
                'message': 'user created',
                'token': jwt_token, 
                'user': self.to_valid_dict_response({**data, '_id': user.inserted_id})
            }, 201
        except Exception as e:
            print(e.__doc__)
            return str(e)
    def sign_in(self, form):
        try:
            
            current_user = self.user_collection.find_one({'email': form['email']})
            if not current_user or not bcrypt.checkpw(bytes(form['password'], 'utf-8'), current_user['password']):
                raise Exception("Kindly enter a valid email or password")
            user = self.to_valid_dict_response(current_user)
            del user['password']
            return {    
                'message': 'succesfully logged in',
                'token': self.create_jwt(user), 
                'user': user
            }, 200
        except Exception as e:
            print(str(e))
            return str(e), 400
        pass

        