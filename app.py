from flask import Flask,request
from flask_restful import Api
from routes import Routes
from flask_cors import CORS
from services.db import mongo
from gevent.pywsgi import WSGIServer
import os
from dotenv import load_dotenv
import ssl

load_dotenv(); 

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://coms-messaging-21078062.com"}})


api = Api(app); 

Routes(api)

if __name__ == "__main__":
    app.config.from_object('settings')
    mongo.init_app(app)
#    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#    context.load_cert_chain('certificate.crt', 'new-coms.key')
#    context.load_verify_locations(cafile="ca_bundle.crt")


    print("running the application")
    http_server = WSGIServer(('', 5001), app)#, ssl_context=context)
    http_server.serve_forever()

    
