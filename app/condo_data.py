from bs4 import BeautifulSoup
import requests
import time
import re
import mechanize
import csv
import os
from io import BytesIO
import zipfile
#import lxml
#from app import app

def scrapeSinglePage(text):
    """Take all of the data from the html table and format it into 
    a list of lists to be easily processed later"""
    #strainer = SoupStrainer('table', attrs={'id': 'form1'})
    #soup = BeautifulSoup(text, "lxml", parse_only=strainer)
    soup = BeautifulSoup(text, "html5lib")
    print(soup)

    table = soup.find_all('table')[4]

    str = ""
    count = 0 
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        temp = ",".join([re.sub('\s{2,}', ' ',x.text) for x in cols]) + "\n"

        if "CondoName" not in temp:
            count+=1
            str += temp

    return str , count


def isThereNext(text):
    """Check there is a Next button on the page."""
    soup = BeautifulSoup(text, "html5lib")

    if("[Next]" in soup.get_text()):

        return True
    return False

def getNext(text,br,num_condos):
    """Get the response from the next page of condo data"""
    br.select_form(nr=2)
    #br.form.find_control("FSTATE").readonly = False
    #br.form.find_control("maxRows").readonly = False
    #br.form.find_control("FSTATE").value = "DC"
    #br.form.find_control("maxRows").value = str(num_condos-50)
    #form.set_all_readonly(False)
    #br.form.controls.FSTATE = ["DC"]
    #control.maxRows = [num_condos-50]
    #for control in br.form.controls:
    #    print control
    response = br.submit(type='image')
    text = response.read()

    return text

def scraperNoScraping(state):
    url = "https://entp.hud.gov/idapp/html/condlook.cfm"
    for x in range(0,5):
        print('\n')
    print("program starting")
    print(state)
    for x in range(0,5):
        print('\n')
    br = mechanize.Browser()
    br.open(url)

    response = br.response()
    

    
    
    br.select_form(name='condoform')
    br.form['fstate'] = [state,]
    response = br.submit()
    text = response.read()

    regex = re.compile(r'[0-9]+ records were selected')
    results = regex.findall(text)

    num_condos = ""
    for x in results:
        num_condos = int(x.split(' ', 1)[0])

    
    filename = state + "_Condo_Data.csv"
    
    count = 0
    ans="CondoName,Condo ID /Submission,Address,County,ApprovalMethod,Compositionof Project,Comments,DocumentStatus,ManufacturedHousing,FHAConcentration,Status,StatusDate,ExpirationDate\n"
    t0 = time.time()
    tup = scrapeSinglePage(text)
    ans += tup[0]  
    count += int(tup[1])
    msg = ""

    while isThereNext(text):
        try:
            text = getNext(text,br,num_condos)

        except:
            msg="Site error occured in reading data for " + state + ", not all data was retrieved."
            break
            
        if len(text)> 0:
            tup = scrapeSinglePage(text)
            ans += tup[0]
            count += int(tup[1])

    d = time.time() - t0
    print "duration: %.2f s." % d

    #with open(app.static_folder+ "/output/" + filename, "wb") as file:
    with open("static/output/" + filename, "wb") as file:
        file.write(ans)
    if count != num_condos:
        msg ="Site error occured in reading data for " + state + ", not all data was retrieved."

    return msg

scraperNoScraping('GU')