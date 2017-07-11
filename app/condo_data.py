from bs4 import BeautifulSoup
import requests
import time
import re
import mechanize
import csv
from selenium import webdriver


def scrapeSinglePage(text, data):
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
            if len(cols) > 4:
                data.append([re.sub('\s+', ' ',x.text.replace("\n","").replace("\t","").replace("  "," ").encode("utf-8").strip('"').strip()) for x in cols])

def isThereNext(text):
    """Check there is a Next button on the page."""
    soup = BeautifulSoup(text, "html5lib")

    if("[Next]" in soup.get_text()):
        return True
    return False

def getNext(text,br):
    """Get the response from the next page of condo data"""
    return

def scraperNoScraping(state):
    url = "https://entp.hud.gov/idapp/html/condlook.cfm"

    br = mechanize.Browser()
    br.open(url)

    response = br.response()
    br.select_form(name='condoform')
    br.form['fstate'] = [state,]
    response = br.submit()
    text = response.read()
    
    data = []
    
    scrapeSinglePage(text,data)

    filename = state + "_Condo_Data.csv"
    with open(filename, "wb") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    
    return filename