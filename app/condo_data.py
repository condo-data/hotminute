from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests
import time
import re
import csv
import mechanize
import types
from app import app

def scrapeSinglePage(text, site, reportType):
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
    if site == 'va' and reportType == 'details':
        for row in rows:
            
            try:
                cols = row.tr.findAll('td')
                #print(cols)
            except:
                continue
            
            if len(cols) > 2:

                temp = ",".join([re.sub('\s{2,}', ' ',x.text).replace(",","") for x in cols]) + ","
               # print(len(temp))
                #print(count)
                str += temp
        
            #print(row)
    else:

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
    return str , count


def isThereNext(text):
    """Check there is a Next button on the page."""
    soup = BeautifulSoup(text)

    if("[Next]" in soup.text):
        return True
    
    return False

def getNext(text,br,num_condos):
    """Get the response from the next page of condo data"""
    br.select_form(nr=2)
    response = br.submit(type='image')
    text = response.read()

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
    
    regex = re.compile(r'[0-9]+ records')
    results = regex.findall(text)
 
    num_condos = ""
    for x in results:
        num_condos = int(x.split(' ', 1)[0])
    
    filename = state + "_Condo_Data.csv"
    count = 0
    t0 = time.time()
    
    if "No records match all the selection criteria" not in text:
        tup = scrapeSinglePage(text,site,reportType)
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
                tup = scrapeSinglePage(text,site, reportType)
                ans += tup[0]
                count += int(tup[1])
                



    else:
        msg = "No records match the selection criteria for " + state + " no data was retrieved."

    d = time.time() - t0
    if site == "va":
         ans = ans.encode('utf-8')
         ans = ans.replace("&nbsp", "")
    print(state +" duration: %.2f s." % d)


    if site == 'va' and reportType == 'details':
        count = 0
    #print(ans)
        mylist = ans.split(",")
        i = 0
        ansl =[]
        temp = []
    
        ansl.append(["Condo Name (ID)","Address,Status","Last Update","Request Received Date","Review Completion Date"])
        #print(mylist)
        mylist = mylist[6:]
        
        for l in mylist:
            if len(l) > 100:
                continue
            #print(l)
            if i == 12:
                #print(temp)
                ansl.append(temp)
                i = 0
            if i == 0:
                temp = []
                #print(temp)

        
            if i % 2 != 0:
            #print(i)
            #print(l)
                temp.append(l)
            i+=1
        count = len(ansl)-1
    #for l in ansl:
    #    print(l)
    #print(len(ansl))
    #print(mylist)
    
    
    if site == "hud":
        reportType = ""
    if site == 'va':
        count -=1
    if count != num_condos:
        msg ="Site error occured in reading data for " + state + ", not all data was retrieved."

    
    
    #with open( os.path.join(path, name) , 'r') as mycsvfile:
#writer = csv.writer(open(newFilename, 'w'))

    with open(app.static_folder+ "/output/" + filename, "wb") as file:
    #with open("static/output/" + filename, "wb") as file:
        if site == 'va' and reportType == 'details':
            writer = csv.writer(file)
            writer.writerows(ansl)
        else:
            file.write(ans)    

    return msg


#if __name__ == "__main__":
    
   
#    print(scraperNoScraping("GU", "hud", ""))
