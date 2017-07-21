from flask import render_template, flash, redirect,request, current_app, url_for,send_from_directory, send_file, jsonify
from app import app
from .forms import CondoForm, DownloadForm
import condo_data
import os
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
import zipfile
from io import BytesIO

#import celery

executor = ThreadPoolExecutor(1)

#@celery.task
#def run_scrape_data(state_selected):
#    condo_data.scraperNoScraping(state_selected)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    global future
    form = CondoForm()

    if form.validate_on_submit():
        
            
        state_selected = request.form['state']
        
        if state_selected == "ALL":
            future = executor.submit( condo_data.getAllStates)
        else:
            future = executor.submit( condo_data.scraperNoScraping, state_selected)
        #condo_data.scraperNoScraping(state_selected)
        #task = run_scrape_data.apply_async(args=[state_selected])
        
        #print("on first page")
        
        #for x in range(0,5):
        #    if future.done():
        #        break
        #    else: 
                #print("first page: sleep for 5 more sec!")
        #        time.sleep(5)
        time.sleep(0)
         
        return redirect(url_for("load", state_selected=state_selected))    
        
        #return redirect(url_for("downloadpage", state_selected=state_selected)) 
 
    return render_template('index.html',form=form)
          
@app.route('/load/<state_selected>', methods=['GET', 'POST'])
def load(state_selected=None):
    #global state_selected
    #print("has gone to next 1")
    #if not future.done():
        #isDone(state_selected,"hey")
    #return redirect(url_for("downloadpage", state_selected=state_selected)) 
    print("what")
    #    for x in range(0,10):
    #        if future.done():
    #            break
    #        else: 
                #print("first page: sleep for 5 more sec!")
    #            time.sleep(5)
        #time.sleep(50)
    return render_template('load.html')
    #print("done 1")
        


    



@app.route('/downloadpage/<state_selected>', methods=['GET', 'POST'])
def downloadpage(state_selected=None):
    print("in the downloads the mighty downloads")
    form = DownloadForm()
    fn = ""
    
    fileType = ""
    
    if state_selected == 'ALL':
        fileType = ".zip"
    else:
        fileType = '.csv'
    
    

    mydate = datetime.datetime.now()
    month = mydate.strftime("%B")
    year = mydate.year
    fn = str(month) + str(year) + "_" + state_selected + "_Condo_Data" + fileType

    
    msgs = future.result()
    #print(msgs)
    
    if form.validate_on_submit():
        #isDone(state_selected, fn)
        return redirect(url_for("download", state_selected=state_selected, filename=fn)) 

    return render_template('download.html',form=form, state_selected=state_selected, filename=fn, msgs=msgs)
    
@app.route('/download/<state_selected>/<filename>', methods=['GET', 'POST'])
def download(state_selected=None, filename=None):
    directory = app.static_folder + "//output//"
    if state_selected == 'ALL':
        memory_file = BytesIO()
        #memory_file = "static/output/All_States.zip"
        files = []
   #     print(app.config['STATES'][selected_state])
    
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
    print(future.done())
    #print("here")
    
    state_selected  = request.args.get('state_selected', None)
    print(state_selected)
   #change  = request.args.get('change', None)
    if future.done():
        return jsonify({'state_selected': state_selected, 'result':url_for("downloadpage", state_selected=state_selected)})
    #else:
    #    return jsonify(result="notdone")
    
@app.route('/echo/', methods=['GET,POST'])
def echo():
    return render_template('temp.html')
    