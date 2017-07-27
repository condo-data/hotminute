from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from app import app
    
class CondoForm(FlaskForm):
    states=app.config['STATES']
    
    state = SelectField(
        'State', 
        choices=states, )
        
    submit = SubmitField()
    
class DownloadForm(FlaskForm):
    submit = SubmitField("Download")