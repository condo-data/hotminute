from bs4 import BeautifulSoup
import requests
import time
import re
import mechanize
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
#from app import app


def scrapeSinglePage(text, data, isFirst):
    """Take all of the data from the html table and format it into 
    a list of lists to be easily processed later"""
    soup = BeautifulSoup(text, "html5lib")

    tables = soup.find_all('table')
    table = []

    #appending data
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            #print(cols)
            if len(cols) > 4:
                #if "CondoName" not in cols:
                data.append([re.sub('\s+', ' ',x.text.replace("\n","").replace("\t","").replace("  "," ").encode("utf-8").strip('"').strip()) for x in cols])
                #print(data)

def isThereNext(text):
    """Check there is a Next button on the page."""
    soup = BeautifulSoup(text, "html5lib")

    if("[Next]" in soup.get_text()):
        print("there is next")
        return True
    return False

def getNext(text,br):
    """Get the response from the next page of condo data"""
    br.select_form(name="getMoreData")
    response = br.submit(type='image')
    text = response.read()
    #print(text)
    
    return text

def scraperNoScraping(state):
    url = "https://entp.hud.gov/idapp/html/condlook.cfm"

    br = mechanize.Browser()
    br.open(url)

    response = br.response()
    br.select_form(name='condoform')
    br.form['fstate'] = [state,]
    response = br.submit()
    text = response.read()
    #print(response)
    
    data = []
    
    scrapeSinglePage(text,data,True)
    count = 1
    while isThereNext(text):
        text = getNext(text,br)
        scrapeSinglePage(text,data,False)
        count+=1
        print(count)
    #print(data)

    filename = "Condo_Data.csv"
    #with open(app.static_folder+ "//" + filename, "wb") as file:
    with open("static//" + filename, "wb") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    
    return filename
    
scraperNoScraping('DC')