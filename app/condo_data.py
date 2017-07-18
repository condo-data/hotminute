from bs4 import BeautifulSoup
import requests
import time
import re
import mechanize
import csv
from app import app



def scrapeSinglePage(text):
    """Take all of the data from the html table and format it into 
    a list of lists to be easily processed later"""
    soup = BeautifulSoup(text, "html5lib")

    table = soup.find_all('table')[4]

    str = ""

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        temp = ",".join([re.sub('\s{2,}', ' ',x.text) for x in cols]) + "\n"

        if "CondoName" not in temp:
            str += temp
    #print(str)

    return str


def isThereNext(text):
    """Check there is a Next button on the page."""
    soup = BeautifulSoup(text, "html5lib")

    if("[Next]" in soup.get_text()):

        return True
    return False

def getNext(text,br):
    """Get the response from the next page of condo data"""
    #br.select_form(name="getMoreData")
    br.select_form(nr=2)
    response = br.submit(type='image')
    text = response.read()
    
    return text

def scraperNoScraping(state):
    url = "https://entp.hud.gov/idapp/html/condlook.cfm"
    print("program starting")
    
    br = mechanize.Browser()
    br.open(url)

    response = br.response()
    br.select_form(name='condoform')
    br.form['fstate'] = [state,]
    response = br.submit()
    text = response.read()
    
    filename = state + "_Condo_Data.csv"

    ans="CondoName,Condo ID /Submission,Address,County,ApprovalMethod,Compositionof Project,Comments,DocumentStatus,ManufacturedHousing,FHAConcentration,Status,StatusDate,ExpirationDate\n"
    t0 = time.time()
    ans += scrapeSinglePage(text)  
    
    count = 0;
    msg = ""
    while isThereNext(text):
        #if response.code == 500:
        #    continue
        count += 1
        try:
            text = getNext(text,br)
            count = 0
            #for form in br.forms():
            #    count+=1
            #    print form
            #    print count
            #print("done")
        except:
            #print("Error: " + str(response.code))
            msg= "Site error occured in reading data for " + state + ", not all data was retrieved."
            break
            
        if len(text)> 0:
            ans += scrapeSinglePage(text)
        #print(count)
    d = time.time() - t0
    print "duration: %.2f s." % d
    
    with open(app.static_folder+ "//output//" + filename, "wb") as file:
    #with open("static/output/" + filename, "wb") as file:
        file.write(ans)
    #print msg
    return msg
def getAllStates():
    states = app.config['STATES']
    #states = [('AK', 'Alaska'),('AL', 'Alabama'),('AR', 'Arkansas'),( 'AZ', 'Arizona'),('CA', 'California'),('CO', 'Colorado'),
    #('CT', 'Connecticut'),('DC', 'District of Columbia'),('DE', 'Delaware'),('FL', 'Florida'),('GA', 'Georgia'), ('GU', 'Guam'),
    #('HI', 'Hawaii'),('IA', 'Iowa'),('ID', 'Idaho'),('IL', 'Illinois'),('IN', 'Indiana'),('KS', 'Kansas'),('KY', 'Kentucky'),
    #('LA', 'Louisiana'),('MA', 'Massachusetts'),('MD', 'Maryland'),('ME', 'Maine'),('MI', 'Michigan'),('MN', 'Minnesota'),
    #('MO', 'Missouri'),('MS', 'Mississippi'),('MT', 'Montana'),('NC', 'North Carolina'),('ND', 'North Dakota'),('NE', 'Nebraska'),
    #('NH', 'New Hampshire'),('NJ', 'New Jersey'),('NM', 'New Mexico'),('NV', 'Nevada'),('NY', 'New York'),('OH', 'Ohio'),
    #('OK', 'Oklahoma'),('OR', 'Oregon'),('PA', 'Pennsylvania'),('PR', 'Puerto Rico'),('RI', 'Rhode Island'),('SC', 'South Carolina'),
    #('SD', 'South Dakota'),('TN', 'Tennessee'),('TX', 'Texas'),('UT', 'Utah'),('VA', 'Virginia'),('VI', 'Virgin Islands'),('VT', 'Vermont'),
    #('WA', 'Washington'),('WI', 'Wisconsin'),('WV', 'West Virginia'),('WY', 'Wyoming')]
    
    t0 = time.time()
    msgs = []
    for x in states:
        print(x[0])
        msgs.append(scraperNoScraping(x[0]))
    d = time.time() - t0
    print "duration of all states : %.2f s." % d
        
    return msgs
#getAllStates()
#scraperNoScraping("")
#print("program done")