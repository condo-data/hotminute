#!flask/bin/python
from app import app
import os

app.run(debug=True,host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
#  <!-----<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}"> 