from flask import Flask
from flask_restful import Api
from routes import Routes
from flask_cors import CORS
from services.db import mongo
from gevent.pywsgi import WSGIServer


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app); 

Routes(api)



if __name__ == "__main__":
    app.config.from_object('settings')
    mongo.init_app(app)
    print("running the application")
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

    
