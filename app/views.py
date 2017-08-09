from flask import render_template, flash, redirect,request, current_app, url_for,send_from_directory, send_file, jsonify
from app import app
from .forms import CondoForm, DownloadForm, VACondoForm
import condo_data
import os
#import time
import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import zipfile
from io import BytesIO
from pympler.tracker import SummaryTracker
import gc
tracker = SummaryTracker()
executor = ProcessPoolExecutor(3)
futures = []
#states = []






@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    global states
    global reportType
    
    directory = app.static_folder + "/output/"
        
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            os.remove(directory + file)
    
    form = CondoForm()
    va_form = VACondoForm()
    
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
                futures.append(executor.submit(condo_data.scraperNoScraping, state[0], site, reportType))
                
         

        else:
            futures.append(executor.submit(condo_data.scraperNoScraping, state_selected, site, reportType))

            
        return redirect(url_for("load", state_selected=state_selected, site=site))    
        
    elif va_form.vasubmit.data and va_form.validate_on_submit():
        site = "va"
        state_selected = request.form.get('state')
        reportType = request.form.get('rt')
        
        if state_selected == "ALL":
            states = app.config["VA_STATES"]
            states = states[1:]
            print(states)
            
            count = 0
            for state in states:
                if count == 5:
                    break
                futures.append(executor.submit(condo_data.scraperNoScraping, state[0], site, reportType))
                states.remove(state)
                count += 1
            print(states)
                
            

        else:
            futures.append(executor.submit(condo_data.scraperNoScraping, state_selected, site, reportType))

        collected = gc.collect()
        print "Garbage collector: collected %d objects." % (collected)
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
    for f in as_completed(futures):
        if len(f.result()) > 1:
            msgs.append(f.result()) 



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
        del files
        
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
    #reportType = request.args.get('reportType', None)
    
    for x in futures:
        if x.done():
            futures.remove(x)
            if state_selected == "ALL" and len(states) > 0:
                print(states[0][0])
                #print(reportType)
                futures.append(executor.submit(condo_data.scraperNoScraping, states[0][0], site, reportType))
                states.remove(states[0])
    print(futures)
    print(states)
    
    if len(futures) < 1:
        del futures[:]  
        
        return jsonify({'state_selected': state_selected, 'result':url_for("downloadpage", state_selected=state_selected, site=site)})