#!flask/bin/python
#from flask import Flask
from app import app
import os

#app = Flask(__name__)
if __name__ == '__main__':
 port = int(os.environ.get("PORT", 5000))
 app.run(host='0.0.0.0', port=port, debug=True)



#app.run(host='0.0.0.0', port=8080, debug=True)




