from flask import render_template, flash, redirect,request, current_app, url_for,send_from_directory
from app import app
from .forms import CondoForm
import condo_data
import os

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    form = CondoForm()

    if form.validate_on_submit():
            
        state_selected = request.form['state']
        fn = condo_data.scraperNoScraping(state_selected)
   
        return redirect(url_for("download", filename=fn))
 
    return render_template('index.html',form=form)
                  
    
       
       
@app.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename=None):
    
    return send_from_directory(directory=app.static_folder, filename=filename)