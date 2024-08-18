from flask_restful import Resource
from flask import request
from services import TwilioClient
from bson.objectid import ObjectId
from util import token_required, Util
from services.db import mongo
import os
from app import limiter
(client, twilio_number, _) = TwilioClient.get_client(TwilioClient); 


class Message(Resource, Util):
    def __init__(self):
        self.group_collection = mongo.db.groups
        self.message_collection = mongo.db.messages
        pass
    @token_required
    def get(self, user):
        try:
            response = []
            # messages = []
            messaging_insights = self.get_messaging_insights()      
            sent_messages = []
            if user['role'] == os.environ['ADMIN']: 
                sent_messages = self.message_collection.find({})
            else:
                sent_messages = self.message_collection.find({'user_id': ObjectId(user['id'])})
            
            # fetches the messages by message id
            # expensive loop as the size of messages grow
            # to be optimized
            for sent_message in sent_messages:
                group = self.group_collection.find_one({'_id': sent_message['group_id']})
                group['id'] = str(group['_id'])
                del group['_id']
                del group['user_id']
                for message in sent_message['messages']:
                    response.extend(
                        map(lambda message: {**message, "group": group}, #adds the group to the response
                            filter(
                            lambda insight: insight['id'] == message['id'],
                            messaging_insights)
                        )
                    )
            
            return response
        except Exception as e:
            print(str(e))
            return str(e),500
         
    @token_required
    @limiter.limit("10 per minute")
    def post(self, user):
        try:           
            form = request.get_json(force=True)
            
            group = self.group_collection.find_one({'_id':ObjectId(form['groupId'])})
            numbers = group['numbers']
            types = form['types']
            response = []
            
            # send messages to all numbers in a group by the type
            for type in types:
                for number in numbers:
                    phone_number = number['code'] + number['number']
                    response.append(self\
                        .handle_message_type(type=type, form=form, 
                                             number=phone_number, user_id=user['id'],
                                             number_object=number))
                
            return response, 201
        except Exception as e:
            print(e.__doc__)
            return {"error": e.__doc__, "data": e.__dict__}, 500
    
    def handle_message_type(self, **kwargs):  
        type, form, number, user_id, number_object = kwargs.values()
        messageBody = self.clean_text(form['body'])
        try: 
            if type == "SMS":
                message = client.messages \
                    .create(
                    body=messageBody,
                    from_= twilio_number,
                    to=number
                    )
                self.handle_store_message(message.sid, form, type, user_id)
                return {f"{type}": message.sid}
            elif type == "TTS":
                call = client.calls.create(
                        twiml=f'<Response><Say>{messageBody}</Say></Response>',
                        to=number,
                        from_= twilio_number,
                    )
                self.handle_store_message(call.sid, form, type)
                
                return {f'{type}': call.sid}
            else:
               message = client.messages.create(
                              body=messageBody,
                              from_=f'whatsapp:{twilio_number}',
                              to=f'whatsapp:{number}'
                          )
               self.handle_store_message(message.sid, form, type, user_id)
               return {f'{type}': message.sid}
        except Exception as e:
                return { f"{number}": {f"{type}": e.__doc__}, 
                        'number':number_object 
                        }, 500         
         
    def handle_store_message(self, message_sid, form, type, user_id):
        self.message_collection\
        .find_one_and_update(
            {'group_id':ObjectId(form['groupId'])},
            {"$push":{'messages':{
            'id': message_sid,
            'type': type
            }
          }, "$set": {"user_id": ObjectId(user_id)}}, upsert=True )
    def get_message_by_id(self, insight, message):
        return  insight['_id'] == message['id'] 
             

# /'+447876159566'