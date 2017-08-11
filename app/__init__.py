from flask import Flask
from flask_compress import Compress

app = Flask(__name__, static_folder='static')
app.config.from_object('config')
Compress(app)

import views
