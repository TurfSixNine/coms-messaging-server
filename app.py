from flask import Flask,request
from flask_restful import Api
from routes import Routes
from flask_cors import CORS
from services.db import mongo
from gevent.pywsgi import WSGIServer
import os
from dotenv import load_dotenv

load_dotenv(); 

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app); 

Routes(api)

# setting up the flask to trust the ELB proxy and handle HTTPS requests
app.config['TRUSTED_PROXIES'] = [os.environ['ELB_DNS']]  # Add your proxy server IP or range

def set_wsgi_url_scheme():
    if request.headers.get('X-Forwarded-Proto', 'http') == 'https':
        request.environ['wsgi.url_scheme'] = 'https'

# Register the set_wsgi_url_scheme function as a before_request handler
app.before_request(set_wsgi_url_scheme)


if __name__ == "__main__":
    app.config.from_object('settings')
    mongo.init_app(app)
    

    print("running the application")
    http_server = WSGIServer(('', 5001), app)
    http_server.serve_forever()

    
