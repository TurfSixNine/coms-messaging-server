import os
import jwt
from datetime import datetime , timedelta
from functools import wraps
from flask_restful import request
import json
from dotenv import load_dotenv
from services import TwilioClient
from html_sanitizer import Sanitizer
import re
sanitizer = Sanitizer()
(client, twilio_number, message_ssid )= TwilioClient.get_client(TwilioClient)

load_dotenv()


class Util:
    def to_valid_dict_response(self, document):
        data = {
                    key : value
                   for key, value in dict(document).items()
                }
        id =  str(data['_id'])
        del data['_id']
        data['id'] = id
        return data
    def clean_text(self, text):
        text = sanitizer.sanitize(text)   
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    def create_jwt(self, data):
       return  jwt.encode({
                'id': data['id'],
                'user': data['username'],
                'email': data['email'],
                'role':data['role'],
                'expiration':str(datetime.now() + timedelta(hours=1))
            },os.environ['JWT_SECRET'])
    def get_messaging_insights(self):
        try:
            # get calls insight
            response = []
            message_summaries = client.messages.list(from_=twilio_number)
            for message in message_summaries:
                response.append({
                    'receipient': message.to,
                    'id': message.sid,
                    'status': message.status,
                    'direction': message.direction,
                    'send_date':message.date_sent.strftime("%m/%d/%Y, %H:%M:%S"),
                    'call_price': message.price,
                    'error_code': message.error_code,
                })
            return response
        except Exception as e:
            str(e)
            return str(e)
    def get_calls_insights(self):
        try:
            # get calls insight
            response = []
            call_summaries = client.calls.list(from_=twilio_number)
            for call in call_summaries:
                response.append({
                    'receipient': call.to,
                    'id': call.sid,
                    'answered_by':call.answered_by,
                    'start_time':call.start_time.strftime("%H:%M:%S"),
                    'start_date':call.start_time.strftime("%m/%d/%Y"),
                    'status': call.status,
                    'direction': call.direction,
                    'duration': call.duration,
                    'end_time':call.end_time.strftime("%H:%M:%S"),
                    'end_date':call.start_time.strftime("%m/%d/%Y"),
                    'call_price': call.price,
                    'currency':call.price_unit,
                
                })
            return response
        except Exception as e:
            print(e.__doc__, dict(e))
            return e.__doc__
    



def token_required(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            payload = None
            token =  request.headers['authorization']
            token = token.split(" ")[1]
            if not token:
                return json.dumps({"message":"kindly pass a token"}), 400
            try:
                payload = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=["HS256"])
                kwargs['user'] = payload
                return func(*args, **kwargs)
            except Exception as e:
                return "Invalid token!!", 451
        return decorated
               