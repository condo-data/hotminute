from flask import render_template, flash, redirect,request, url_for
from app import app
from .forms import  CondoForm
#from requests import request


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = CondoForm()
    if request.method == 'POST':
        print("hey")
        if form.validate_on_submit():
            print("submitted")
            data = request.form['state']
            print(url_for('download'))
            return render_template('download.html')
            #redirect(url_for('download'))
        print("why")
    print("hey2")
    return render_template('index.html',
                           title='Condo Form',
                           form=form)
                  
       
@app.route('/download', methods=['GET', 'POST'])   
def download():
    print("help")
    #return "hey"
    return render_template('download.html')