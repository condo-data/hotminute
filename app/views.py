from flask import render_template, flash, redirect,request, current_app, url_for,send_from_directory, send_file, jsonify
from app import app
from .forms import CondoForm, DownloadForm, VACondoForm
import condo_data
import os
import time
import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import zipfile
from io import BytesIO
executor = ProcessPoolExecutor(4)
futures = []


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    form = CondoForm()
    va_form = VACondoForm()
    
    #futures = []
    futures[:] = []
    if form.submit1.data and form.validate_on_submit():
        state_selected = request.form['state']
        reportType = ""
        print(reportType)
        site = "hud"
        if state_selected == "ALL":
            states = app.config["STATES"]
            states = states[1:]
            
            for state in states:
                future = executor.submit(condo_data.scraperNoScraping, state[0], site, reportType)
                futures.append(future)

        else:
            future = executor.submit(condo_data.scraperNoScraping, state_selected, site, reportType)
            futures.append(future)

        
        return redirect(url_for("load", state_selected=state_selected, site=site))    
        
    elif va_form.vasubmit.data and va_form.validate_on_submit():
        site = "va"
        state_selected = request.form.get('state')
        reportType = request.form.get('rt')
        print(state_selected)
        
        if state_selected == "ALL":
            states = app.config["VA_STATES"]
            states = states[1:]
            
            for state in states:
                future = executor.submit(condo_data.scraperNoScraping, state[0], site, reportType)
                futures.append(future)

        else:
            future = executor.submit(condo_data.scraperNoScraping, state_selected, site, reportType)
            futures.append(future)

        
        return redirect(url_for("load", state_selected=state_selected,site=site))    
 
    return render_template('index.html',form=form, va_form=va_form)
          
@app.route('/load/<state_selected>/<site>', methods=['GET', 'POST'])
def load(state_selected=None,site=None):
    return render_template('load.html', state_selected=state_selected,site=site)
        
@app.route('/downloadpage/<state_selected>/<site>', methods=['GET', 'POST'])
def downloadpage(state_selected=None, site=None):
    
    form = DownloadForm()
    fn = ""
    msgs = []
    fileType = ""
    origin = site.upper()
    
    
    if state_selected == 'ALL':
        fileType = ".zip"
    else:
        fileType = '.csv'
    
    mydate = datetime.datetime.now()
    month = mydate.strftime("%B")
    day = mydate.strftime('%d')
    year = mydate.year
    fn = str(month) +  "_" +  str(day)+ "_" + str(year) + "_" + state_selected + "_" + origin + "_Condo_Data" + fileType

    #get all messages 
    for x in futures:
        #print(x.result)
        #print(x.result)
        if len(x.result()) > 1:
            
            msgs.append(x.result()) 
            #print(msgs)
    
    if form.validate_on_submit():
        return redirect(url_for("download", state_selected=state_selected, filename=fn)) 

    return render_template('download.html',form=form, state_selected=state_selected, filename=fn, msgs=msgs, site=site)
    
@app.route('/download/<state_selected>/<filename>', methods=['GET', 'POST'])
def download(state_selected=None, filename=None):
    directory = app.static_folder + "/output/"
    if state_selected == 'ALL':
        memory_file = BytesIO()
        files = []
        
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                files.append(os.path.join(file))
  
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for individualFile in files:
                zf.write(directory + individualFile, "/"+individualFile)

        memory_file.seek(0)
        return send_file(memory_file, attachment_filename=filename, as_attachment=True)
    else: 
        attachment_filename = filename
        
    fn = state_selected + "_Condo_Data.csv"
    return send_from_directory(directory=directory, filename=fn, as_attachment=True, attachment_filename=attachment_filename)

@app.route('/done/', methods=['GET', "POST"])
def isDone():
    state_selected  = request.args.get('state_selected', None)
    site  = request.args.get('site', None)
    
    #print(futures.ALL_C)

    isDone = set([x.done() for x in futures])
    
    if len(isDone) == 1 and True in isDone:
        print(futures)
        del futures[:]  
        print(futures)
        return jsonify({'state_selected': state_selected, 'result':url_for("downloadpage", state_selected=state_selected, site=site)})