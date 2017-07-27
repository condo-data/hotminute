from flask import render_template, flash, redirect,request, current_app, url_for,send_from_directory, send_file, jsonify
from app import app
from .forms import CondoForm, DownloadForm
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

    if form.validate_on_submit():
        
        state_selected = request.form['state']
        
        if state_selected == "ALL":
            states = app.config["STATES"]
            states = states[1:]
            
            for state in states:
                future = executor.submit(condo_data.scraperNoScraping, state[0])
                futures.append(future)

        else:
            future = executor.submit( condo_data.scraperNoScraping, state_selected)
            futures.append(future)

        time.sleep(0)
         
        return redirect(url_for("load", state_selected=state_selected))    
 
    return render_template('index.html',form=form)
          
@app.route('/load/<state_selected>', methods=['GET', 'POST'])
def load(state_selected=None):
    return render_template('load.html')
        
@app.route('/downloadpage/<state_selected>', methods=['GET', 'POST'])
def downloadpage(state_selected=None):
    form = DownloadForm()
    fn = ""
    msgs = []
    fileType = ""
    
    if state_selected == 'ALL':
        fileType = ".zip"
    else:
        fileType = '.csv'
    
    mydate = datetime.datetime.now()
    month = mydate.strftime("%B")
    year = mydate.year
    fn = str(month) + str(year) + "_" + state_selected + "_Condo_Data" + fileType

    #get all messages 
    for x in futures:
        if len(x.result()) > 0:
            msgs.append(x.result()) 
            print(msgs)
    
    if form.validate_on_submit():
        return redirect(url_for("download", state_selected=state_selected, filename=fn)) 

    return render_template('download.html',form=form, state_selected=state_selected, filename=fn, msgs=msgs)
    
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
    isDone = set([x.done() for x in futures])
    
    if len(isDone) == 1 and True in isDone:
        return jsonify({'state_selected': state_selected, 'result':url_for("downloadpage", state_selected=state_selected)})