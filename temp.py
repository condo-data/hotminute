from bs4 import BeautifulSoup
import requests
import time
import re
import mechanize
import urllib

url = "https://entp.hud.gov/idapp/html/condlook.cfm"
print("program starting")
    
#br = mechanize.Browser()
#br.open(url)

#response = br.response()
#br.select_form(name='condoform')
#br.form['fstate'] = ["AZ",]
#response = br.submit()

#br = mechanize.Browser()
parameters = {u"FAPPROVAL_METHOD" : "NEW",
          u"FSORTED_BY" : "condo_name",
          u"FSTATE" : "AZ",
          u"FSTATUS_CODE" : "X",
          u"FSEARCH_TYPE" : "P",
          u"CAME_FROM" : "oth",
          u"IN_FHAC" : "true",
          u"startAt" : "1",
          u"maxRows" : "50",
          u"x" : "60",
          u"y" : "11",
         }  
data = urllib.urlencode(parameters)

cookies = {'CFID': 'Ztnvuwc184uwwru0c4h7aruko518g08e0wd9fb7uoq4wxpg1rn-3470518',
    "CFTOKEN" : "Ztnvuwc184uwwru0c4h7aruko518g08e0wd9fb7uoq4wxpg1rn-5acadfdbbfbcc7b9-2388B94C-F267-98C7-EB780C3C000A8DAB",
    '_sm_au_c': "iHVNDR53P3PjR2sJ08",
}
text = requests.post(url, data=parameters, cookies=cookies).text
#post_url = 
#post_url = "https://entp.hud.gov/idapp/html/condo1.cfm"
#br.open(post_url,data)
#print(response.read())
#response = requests.post(response.geturl(), data=data)
#print(response)
#for c in response.cookies:
#    print(c.name, c.value)

#text = response.text

#request = mechanize.Request(response)
#text = browser.operesponse.geturl()n(response, data=data).read()
#print(text)


#text = br.open(response.geturl(),data ).read()
#print cool
soup = BeautifulSoup(text, "html5lib")

tables = soup.find_all('table')
for table in tables:
    str = ""
    count = 0 
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        temp = ",".join([re.sub('\s{2,}', ' ',x.text) for x in cols]) + "\n"

        if "CondoName" not in temp:
            print(temp)