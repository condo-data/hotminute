from flask import render_template, flash, redirect,request, current_app, url_for,send_from_directory
from app import app
from .forms import CondoForm, DownloadForm
import condo_data
import os
import datetime


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    form = CondoForm()

    if form.validate_on_submit():
            
        state_selected = request.form['state']
        condo_data.scraperNoScraping(state_selected)
   
        return redirect(url_for("downloadpage", state_selected=state_selected)) 
 
    return render_template('index.html',form=form)
                  
        
@app.route('/downloadpage/<state_selected>', methods=['GET', 'POST'])
def downloadpage(state_selected=None):
    
    form = DownloadForm()
    
    mydate = datetime.datetime.now()
    month = mydate.strftime("%B")
    year = mydate.year
    fn = str(month) + str(year) + "_" + state_selected + "_Condo_Data.csv"
    
    
    if form.validate_on_submit():
    
        return redirect(url_for("download", state_selected=state_selected, filename=fn)) 

    return render_template('download.html',form=form, state_selected=state_selected, filename=fn)
    
@app.route('/download/<state_selected>/<filename>', methods=['GET', 'POST'])
def download(state_selected=None, filename=None):
    attachment_filename = filename
    fn = "Condo_Data.csv"
    return send_from_directory(directory=app.static_folder, filename=fn, as_attachment=True, attachment_filename=attachment_filename)