import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class TwilioClient:
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    __account_sid = os.environ['TWILIO_ACCOUNT_SID']
    __auth_token = os.environ['TWILIO_AUTH_TOKEN']
    __twilio_number= os.environ['TWILIO_ACCOUNT_NUMBER']
    __twilio_messaging_sid = os.environ['TWILIO_MESSAGING_SID']
    __client = Client(username=__account_sid, password=__auth_token)
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_client(self):
        return (self.__client,self.__twilio_number, self.__twilio_messaging_sid)

 