from flask import Flask
from flask_compress import Compress


#app.config.from_object('config')
#Compress(app)

compress = Compress()

def start_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object('config')
    compress.init_app(app)
    return app

import views
