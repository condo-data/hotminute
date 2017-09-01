#!flask/bin/python
from app import app
import os
from waitress import serve

if __name__ == '__main__':
 port = int(os.environ.get("PORT", 5000))
 #app.run(host='0.0.0.0', port=port, debug=True)
 serve(app, host='0.0.0.0', port=port)

#if __name__ == '__main__':
# app.run(host='0.0.0.0', port=8080, debug=True)

#new relic key
#639164c532469eb23865fd8385f699f7b3104a95