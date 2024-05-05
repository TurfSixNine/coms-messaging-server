from flask import Flask
from flask_restful import Api
from routes import Routes
from flask_cors import CORS
from services.db import mongo
from gevent.pywsgi import WSGIServer
import ssl

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app); 

Routes(api)



if __name__ == "__main__":
    app.config.from_object('settings')
    mongo.init_app(app)
    #setting up ssl:
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/pki/tls/certs/csr.pem', '/etc/pki/tls/certs/custom.key')

    print("running the application")
    http_server = WSGIServer(('', 5001), app, ssl_context=context)
    http_server.serve_forever()

    
