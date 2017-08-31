from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, RadioField, StringField
from app import app
    
class CondoForm(FlaskForm):
    states=app.config['STATES']
    
    email = StringField()
    
    state = SelectField(
        'State', 
        choices=states, )
        
    submit1 = SubmitField('Get HUD.gov data')

class VACondoForm(FlaskForm):
    states=app.config['VA_STATES']
    
    email = StringField()
    
    state = SelectField(
        'State', 
        choices=states, )
        
    rt = RadioField('Report Type', choices=[('summary','summary'),('details','details')])

        
    vasubmit = SubmitField('Get VA.gov data')
    
class DownloadForm(FlaskForm):
    submit = SubmitField("Download")