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
    scrapeSinglePage(text)  
    
    count = 0;

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
            print("Error: " + str(response.code))
            text = ""
            
        if len(text)> 0:
            ans += scrapeSinglePage(text)
        #print(count)
    d = time.time() - t0
    print "duration: %.2f s." % d
    
    with open(app.static_folder+ "//output//" + filename, "wb") as file:
    #with open("static/" + filename, "wb") as file:
        file.write(ans)
    
#scraperNoScraping("")
#print("program done")