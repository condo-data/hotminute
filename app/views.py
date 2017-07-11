from flask import render_template, flash, redirect,request, url_for
from app import app
from .forms import CondoForm
import condo_data


@app.route('/', methods=['GET', 'POST'])
def index():
    
    form = CondoForm()

    if request.method == 'POST':
        print("j")
        if form.validate_on_submit():
            
            state_selected = request.form['state']
            print(state_selected)
            
            fn = "issa working"
            
            return redirect(url_for("index") + "#myModal")
 
    return render_template('index.html',form=form)
                  
       
@app.route('/download/<filename>', methods=['GET','POST'])   
def download(filename=None):
    print(filename + " hey")
    return "HEY"