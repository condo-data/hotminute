from flask import Flask
from flask_compress import Compress
from flask_mail import Mail


app = Flask(__name__, static_folder='static')
app.config.from_object('config')

Compress(app)
mail = Mail(app)


import views
