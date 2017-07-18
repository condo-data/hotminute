from flask import render_template, flash, redirect,request, current_app, url_for,send_from_directory
from app import app
from .forms import CondoForm, DownloadForm
import condo_data
import os
import time
import datetime
from concurrent.futures import ThreadPoolExecutor

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
        time.sleep(40)
            
        
        return redirect(url_for("loadpage_1", state_selected=state_selected)) 
 
    return render_template('index.html',form=form)
                  

@app.route('/loadpage_1/<state_selected>', methods=['GET', 'POST'])
def loadpage_1(state_selected=None):
    
    #print("has gone to next 1")
    if not future.done():
    #    for x in range(0,10):
    #        if future.done():
    #            break
    #        else: 
                #print("first page: sleep for 5 more sec!")
    #            time.sleep(5)
        time.sleep(40)
    #print("done 1")

    
    return redirect(url_for("loadpage_2", state_selected=state_selected))
    
@app.route('/loadpage_2/<state_selected>', methods=['GET', 'POST'])
def loadpage_2(state_selected=None):
    
    #print("has gone to next 2")
    print(future.done())
    while not future.done():
        pass
    #print("done 2")

    
    return redirect(url_for("downloadpage", state_selected=state_selected))


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
    fn = state_selected + "_Condo_Data.csv"
    return send_from_directory(directory=app.static_folder + "//output//", filename=fn, as_attachment=True, attachment_filename=attachment_filename)