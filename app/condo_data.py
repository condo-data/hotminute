from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests
import time
import re
import mechanize
import csv
import os
#import urllib
from io import BytesIO
import zipfile
#import lxml
from app import app

def scrapeSinglePage(text, site):
    """Take all of the data from the html table and format it into 
    a list of lists to be easily processed later"""
    if site == "hud":
        strainer = SoupStrainer('table', {'width':"100%", 'border':"1", 'cellpadding':"2", 'cellspacing':"1"})
        #"
    else:
        strainer = SoupStrainer('table', {"id":"searchForm:mainpanel", "cellpadding":"10", "cellspacing":"0", "class":"inputpanel"})
    soup = BeautifulSoup(text, parseOnlyThese=strainer)
    
    #soup = BeautifulSoup(text)
    #print(soup)
    #print(soup)

    #table = 
    #for tr in table:
    #    print(tr)
    

    str = ""
    count = 0 
    rows = soup.table.findAll('tr')
    for row in rows:
        cols = row.findAll('td')
        temp = ",".join([re.sub('\s{2,}', ' ',x.text).replace(",","") for x in cols]) + "\n"
        if site == "hud":
            if "CondoName" not in temp:
                count+=1
                str += temp
        else:
            #print(temp)
            if "," in temp and "Your search returned" not in temp and "Condo Name" not in temp:
                count+=1
                #print(temp)
                #temp = temp.replace(",", "")
                str += temp
            #print(str)

    return str , count


def isThereNext(text):
    """Check there is a Next button on the page."""
    soup = BeautifulSoup(text)
    #print(soup.text)

    if("[Next]" in soup.text):
        #print("wat")
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

def scraperNoScraping(state, site, reportType):
    if site == "va":
        url = "https://vip.vba.va.gov/portal/VBAH/VBAHome/condopudsearch?paf_portalId=default&paf_communityId=100002&paf_pageId=500002&paf_dm=full&paf_gear_id=800001&paf_gm=content&paf_ps=_rp_800001_condoName%3D1_%26_rp_800001_condoId%3D1_%26_ps_800001%3Dmaximized%26_pid%3D800001%26_rp_800001_county%3D1_%26_rp_800001_stateCode%3D1_" + state + "%26_pm_800001%3Dview%26_md_800001%3Dview%26_rp_800001_cpbaction%3D1_performSearchPud%26_st_800001%3Dmaximized%26_rp_800001_reportType%3D1_" + reportType + "%26_rp_800001_regionalOffice%3D1_%26_rp_800001_city%3D1_&_requestid=455594"
        if reportType == "details":
            ans = ""
        else:
            ans = "Condo Name,ID,Record Type\n"
    else:
        url = "https://entp.hud.gov/idapp/html/condlook.cfm"
        ans="CondoName,Condo ID /Submission,Address,County,ApprovalMethod,Compositionof Project,Comments,DocumentStatus,ManufacturedHousing,FHAConcentration,Status,StatusDate,ExpirationDate\n"

    #print('\n')
    #print("program starting")
    #print(state)
    #print('\n')
    br = mechanize.Browser()
    br.open(url)

    response = br.response()
    

    
    
    if site == "hud":
        br.select_form(name='condoform')
        br.form['fstate'] = [state,]
        response = br.submit()

    text = response.read()
    


    regex = re.compile(r'[0-9]+ records')
    results = regex.findall(text)
    #print results
    #Your search returned 591 records

    num_condos = ""
    for x in results:
        num_condos = int(x.split(' ', 1)[0])
    #print(num_condos)

    
    filename = state + "_Condo_Data.csv"
    
    count = 0
    #t0 = time.time()
    if "No records match all the selection criteria" not in text:
        tup = scrapeSinglePage(text,site)
  
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
                tup = scrapeSinglePage(text,site)
                ans += tup[0]
                count += int(tup[1])

       

        if site == "hud":
            reportType = ""
            
        if count != num_condos and reportType != "details":
            msg ="Site error occured in reading data for " + state + ", not all data was retrieved."
        elif count != num_condos*5:
            msg ="Site error occured in reading data for " + state + ", not all data was retrieved."
            #print(count)
            #print(num_condos)
    else:
        msg = "No records match the selection criteria for " + state + " no data was retrieved."
    #d = time.time() - t0
    if site == "va":
         ans = ans.encode('utf-8')
         ans = ans.replace("&nbsp", "")
    #print(ans)
    #print state +"duration: %.2f s." % d
    with open(app.static_folder+ "/output/" + filename, "wb") as file:
    #with open("static/output/" + filename, "wb") as file:
        file.write(ans)    
    #print(msg)
    return msg

#scraperNoScraping('AK', "va", "details")
#('AK', "va")