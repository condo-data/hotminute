from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests
import time
import re
import csv
import mechanize
import types
from app import app

def scrapeSinglePage(text, site):
    """Take all of the data from the html table and format it into 
    a list of lists to be easily processed later"""
    if site == "hud":
        strainer = SoupStrainer('table', {'width':"100%", 'border':"1", 'cellpadding':"2", 'cellspacing':"1"})
    else:
        strainer = SoupStrainer('table', {"id":"searchForm:mainpanel", "cellpadding":"10", "cellspacing":"0", "class":"inputpanel"})
    soup = BeautifulSoup(text, parseOnlyThese=strainer)

    str = ""
    count = 0 
    rows = soup.table.findAll('tr')

    for row in rows:
        cols = row.findAll('td')
        temp = ",".join([re.sub('\s{2,}', ' ',x.text).replace(",","") for x in cols]) + "\n"

        if site == "hud":
            if "CondoName" not in temp:
                str += temp
                count +=1 
        else:
            if "," in temp and "Your search returned" not in temp:
                count+=1
                #print(count)
                str += temp
    #print(str)
    soup.decompose()
    return str , count
    
def scrapeSinglePageDetails(text, site):
    """Take all of the data from the html table and format it into 
    a list of lists to be easily processed later"""
    if site == "hud":
        strainer = SoupStrainer('table', {'width':"100%", 'border':"1", 'cellpadding':"2", 'cellspacing':"1"})
    else:
        strainer = SoupStrainer('table', {"id":"searchForm:mainpanel", "cellpadding":"10", "cellspacing":"0", "class":"inputpanel"})
    soup = BeautifulSoup(text, parseOnlyThese=strainer)

    temp = ""
   
    rows = soup.table.findAll('tr')

    for row in rows:
            
        try:
            cols = row.tr.findAll('td')

        except:
            continue
            
        if len(cols) > 2:

            temp = [re.sub('\s{2,}', ' ',x.text).replace(",","") for x in cols]

    i = 0
    ansl =[]
    ansl.append(["Condo Name (ID)","Address,Status","Last Update","Request Received Date","Review Completion Date"])
 
    temp = temp[6:]
    t =[]
    for l in temp:
        if len(l) > 100:
            continue
     
        if i == 12:
            ansl.append(t)
            i = 0
            
        if i == 0:
            t = []

        if i % 2 != 0:
            #print(i)
            #print(l)
            t.append(l)
        i+=1
        
    count = len(ansl)
    #print(count)

    return ansl , count

def scrapeSinglePageDetails2(text, site):
    """Take all of the data from the html table and format it into 
    a list of lists to be easily processed later"""
    if site == "hud":
        strainer = SoupStrainer('table', {'width':"100%", 'border':"1", 'cellpadding':"2", 'cellspacing':"1"})
    else:
        strainer = SoupStrainer('table', {"id":"searchForm:mainpanel", "cellpadding":"10", "cellspacing":"0", "class":"inputpanel"})
    soup = BeautifulSoup(text, parseOnlyThese=strainer)

    ans = ""
   
    rows = soup.table.findAll('tr')
    
    #print(rows[2])
    count = 0
    cols = rows[2].findAll('td')
    #print(cols)
            #ans = ans
    temp = [re.sub('\s{2,}', ' ',x.text).replace(",","").replace("&nbsp", "") for x in cols]
    temp = temp[6:]
        #count = len(temp)
    soup.decompose()
            
    for i in range(0,len(temp)-1):
            
            #",Last Update,Request Received Date,Review Completion Date"
        if "Condo Name (ID)" in temp[i] or "Status" in temp[i] or "Address" in temp[i] or "Last Update" in temp[i] or "Last Update" in temp[i] or "Request Received Date"in temp[i]:
            if "Condo Name" in str(temp[i+1]):
                continue
            ans += str(temp[i+1]) + ','
        elif "Review Completion Date" in temp[i]:
            ans += str(temp[i+1]) + '\n'
            count +=1
            #print(ans)
                    
                    
            #temp = [re.sub('\s{2,}', ' ',x.text).replace(",","") for x in cols]

    
    return ans , count

def isThereNext(text):
    """Check there is a Next button on the page."""
    soup = BeautifulSoup(text)

    if("[Next]" in soup.text):
        return True
    soup.decompose()
    return False

def getNext(text,br,num_condos):
    """Get the response from the next page of condo data"""
    br.select_form(nr=2)
    response = br.submit(type='image')
    text = response.read()
    response.close()
    br.clear_history()
    return text

def scraperNoScraping(state, site, reportType):
    print(state + " program starting")
    
    if site == "va":
        url = "https://vip.vba.va.gov/portal/VBAH/VBAHome/condopudsearch?paf_portalId=default&paf_communityId=100002&paf_pageId=500002&paf_dm=full&paf_gear_id=800001&paf_gm=content&paf_ps=_rp_800001_condoName%3D1_%26_rp_800001_condoId%3D1_%26_ps_800001%3Dmaximized%26_pid%3D800001%26_rp_800001_county%3D1_%26_rp_800001_stateCode%3D1_" + state + "%26_pm_800001%3Dview%26_md_800001%3Dview%26_rp_800001_cpbaction%3D1_performSearchPud%26_st_800001%3Dmaximized%26_rp_800001_reportType%3D1_" + reportType + "%26_rp_800001_regionalOffice%3D1_%26_rp_800001_city%3D1_&_requestid=455594"
        if reportType == "details":
            ans = ""
        else:
            ans = ""
    else:
        url = "https://entp.hud.gov/idapp/html/condlook.cfm"
        ans="CondoName,Condo ID /Submission,Address,County,ApprovalMethod,Compositionof Project,Comments,DocumentStatus,ManufacturedHousing,FHAConcentration,Status,StatusDate,ExpirationDate\n"
    
    br = mechanize.Browser()
    response = br.open(url)
    
    if site == "hud":
        br.select_form(name='condoform')
        br.form['fstate'] = [state,]
        response = br.submit()
        
    text = response.read()
    response.close()
    br.clear_history()
    
    regex = re.compile(r'[0-9]+ records')
    results = regex.findall(text)
 
    num_condos = ""
    for x in results:
        num_condos = int(x.split(' ', 1)[0])
    
    filename = state + "_Condo_Data.csv"
    count = 0
    t0 = time.time()
    
    if "No records match all the selection criteria" not in text and reportType != "details" and site != "va":
        tup = scrapeSinglePage(text,site)
        ans += tup[0]  
        count += int(tup[1])
        msg = ""
        if site == "hud":
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
                



    else:
        msg = "No records match the selection criteria for " + state + " no data was retrieved."

    d = time.time() - t0
    if site == "va":
         ans = ans.encode('utf-8')
         ans = ans.replace("&nbsp", "")
    print(state +" duration: %.2f s." % d)

    ansl = []
    if site == 'va' and reportType == 'details':
        tup = scrapeSinglePageDetails2(text,site)
        ans = tup[0]
        count = int(tup[1])
        #singleScrapePageDetails(text, site)

    
    
    #print(count)
    #print(num_condos)
    if site == "hud":
        reportType = ""
    if site == 'va' and reportType != "details":
        count -=1
    #print(count)
    #print(num_condos)
    if count != num_condos:
        msg ="Site error occured in reading data for " + state + ", not all data was retrieved."

    with open(app.static_folder+ "/output/" + filename, "wb") as file:
    #with open("static/output/" + filename, "wb") as file:
        #if site == 'va' and reportType == 'details':
        #    writer = csv.writer(file)
        #    writer.writerows(ansl)
        #else:
            file.write(ans)    

    return msg


#if __name__ == "__main__":
#    print(scraperNoScraping("DC", "hud", ""))
  #  print(scraperNoScraping("GU", "va", "details"))
    #print(scraperNoScraping("GU", "va", "summary"))
