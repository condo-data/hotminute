from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from app import app
    
class CondoForm(FlaskForm):
    states=app.config['STATES']
    
    state = SelectField(
        'State', 
        choices=states, )
        
    submit1 = SubmitField('Get HUD.gov data')

class VACondoForm(FlaskForm):
    states=app.config['VA_STATES']
    
    state = SelectField(
        'State', 
        choices=states, )
        
    vasubmit = SubmitField('Get VA.gov data')
    
class DownloadForm(FlaskForm):
    submit = SubmitField("Download")