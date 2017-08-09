#!flask/bin/python
from app import app
import os

if __name__ == '__main__':
 port = int(os.environ.get("PORT", 5000))
 app.run(host='0.0.0.0', port=port, debug=True)

#if __name__ == '__main__':
# app.run(host='0.0.0.0', port=8080, debug=True)


#639164c532469eb23865fd8385f699f7b3104a95
