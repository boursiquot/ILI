import urllib2 as url
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime as dt
import logging as lg
import sys
import numpy as np
import smtplib
from email.mime.text import MIMEText


start = dt.datetime.now().strftime("%Y/%m/%d %H:%M")

date = dt.date.today().strftime("%Y%m%d")

textfile = "Z:\\output\\textfile.txt"


logname = "Z:\\logs\\" + "ilinet " + date + ".txt"

lg.basicConfig(filename=logname,level=lg.INFO,filemode = "w")


mmwr = pd.read_csv("Z:\output\mmwrweekno.csv", header = 0, dtype = {"satendwk_days" : int}, delimiter = ",") 


epoch = dt.datetime.utcfromtimestamp(0)

today = dt.datetime.today()

delta = today - epoch

delta = delta.days


mmwr["delta"] = delta

week = pd.DataFrame()

mmwr["week"] =  np.logical_and(mmwr["delta"]  >= mmwr["sunbeginwk_days"], mmwr["satendwk_days"] >= mmwr["delta"])

week = int(mmwr[(mmwr["week"] == True)].literal_wkx.item())

fluyear  = mmwr[(mmwr["week"] == True)].FluYearText.item()



if len(str(week)) == 1:
    week = "0" + str(week-2)


else:
    week = str(int(week)-2) 
	

site = "https://www.cdc.gov/flu/weekly/weeklyarchives" + str(fluyear) + "/data/senAllregt" + str(week) + ".html"

try:

    page = url.urlopen(site)
    lg.info ("ILI Net data checked at {0}.".format(start))

except url.HTTPError as err:

    lg.error(err) 
    print "Error occurred; check log; attemtped to access" + site

    fp = open(textfile, "rb")
    msg = MIMEText(fp.read())
    fp.close()

    msg["Subject"] = "Error occurred; check log; attemtped to access" + site
    msg["From"] = "bernice.boursiquot@ihs.gov"
    msg["To"] = "bernice.boursiquot@ihs.gov"

    s = smtplib.SMTP("localhost")
    s.sendmail("bernice.boursiquot@ihs.gov","bernice.boursiquot@ihs.gov", msg.as_string())
    s.quit()
    
    sys.exit(1) ## From Python docs: a zero value is considered to be a sucessful termination
                ## A non-zero value is considered to be an abnormal termination

soup = bs(page,"html.parser") 

table_headers = soup.findAll("tr",limit = 2)[0].findAll("th")

column_headers = [th.getText() for th in soup.findAll("tr",limit = 2)[0].findAll("th")]

column_headers.insert(0,"Region Type")

column_headers.insert(1,"Region")

column_headers.insert(2,"Year")

column_headers.insert(3,"Num. of Providers")

data_rows = soup.findAll("tr")[1:]

ili_data = [[td.getText() for td in data_rows[i].findAll("td")] for i in range(len(data_rows))]

for i in ili_data:
    x = str(i[0])
    i.pop(0) 
    year = x[0:4]
    week = x[4:]
    i.insert(0,year)
    i.insert(1,week)
    i.insert(0,"National")
    i.insert(1,"X")
    i.insert(3,"X")

df  = pd.DataFrame(ili_data, columns = column_headers)


df["Age 25-49"] = df["Age 25-49"].astype(str).astype(int) #Must convert object type to string type then to integer type


df["Age 50-64"] = df["Age 50-64"].astype(str).astype(int)


df["Week"] = df["Week"].astype(str).astype(int)


df["Year"] = df["Year"].astype(str).astype(int)


df = df.rename(columns = {"Age over 64": "Age 65" ,"Total ILI": "ILLTotal", "% Weighted ILI": "%Weighted ILI",
"% Uweighted ILI": "%UWeighted ILI"})


df["Age 25-64"] = df["Age 25-49"] + df["Age 50-64"]


df[["Region Type", "Region","Year","Week","%Weighted ILI","% Unweighted ILI","Age 0-4","Age 25-49","Age 25-64","Age 5-24","Age 50-64",
"Age 65","Num. of Providers","Total Patients"]]


last_wk = today - dt.timedelta(days = 7)


last_wk = last_wk.strftime("%Y%m%d")


last_wk_file = "Z:\output\_ILINett - "+ last_wk + ".txt"


df_previous = pd.read_csv(last_wk_file , header = 0,  delimiter = ",", dtype = {"Week" : int ,"Year": int}) 


df_previous = df_previous.append(df)


df_previous = df_previous.drop_duplicates(["Year","Week"])


columns_out = ["Region Type", "Region","Year","Week","%Weighted ILI","% Unweighted ILI","Age 0-4","Age 25-49","Age 25-64","Age 5-24","Age 50-64",
"Age 65","Num. of Providers","Total Patients"]

filename = "Z:\\output\\_ILINett - " + date + ".txt"

filename2 =  "Z:\\output\\ILINett.txt"


try:

    df.to_csv(filename, sep=',',columns = columns_out, index = False)
    lg.info("ILI Net data for week " + week + " were sucessfully scraped and exported")

    fp = open(textfile, "rb")
    msg = MIMEText(fp.read())
    fp.close()

    msg["Subject"] = "ILI Net data for week " + week + " were sucessfully scraped and exported"
    msg["From"] = "bernice.boursiquot@ihs.gov"
    msg["To"] = "bernice.boursiquot@ihs.gov"

    s = smtplib.SMTP("localhost")
    s.sendmail("bernice.boursiquot@ihs.gov","bernice.boursiquot@ihs.gov", msg.as_string())
    s.quit()	
   
except:

    lg.info("Issue with scraping and exporting data for week " + week)


    fp = open(textfile, "rb")
    msg = MIMEText(fp.read())
    fp.close()

    msg["Subject"] = "Issue with scraping and exporting data for week " + week
    msg["From"] = "bernice.boursiquot@ihs.gov"
    msg["To"] = "bernice.boursiquot@ihs.gov"

    s = smtplib.SMTP("localhost")
    s.sendmail("bernice.boursiquot@ihs.gov","bernice.boursiquot@ihs.gov", msg.as_string())
    s.quit()

try:
    df_previous.to_csv(filename2, sep=',',columns = columns_out, index = False)
    lg.info("Complete ILINett text file updated suceessfully")
    
    fp = open(textfile, "rb")
    msg = MIMEText(fp.read())
    fp.close()

    msg["Subject"] = "Complete ILINett text file updated suceessfully"
    msg["From"] = "bernice.boursiquot@ihs.gov"
    msg["To"] = "bernice.boursiquot@ihs.gov"

    s = smtplib.SMTP("localhost")
    s.sendmail("bernice.boursiquot@ihs.gov","bernice.boursiquot@ihs.gov", msg.as_string())
    s.quit()

except:

    lg.info("Issue with exporting complete ILINett text file")

    fp = open(textfile, "rb")
    msg = MIMEText(fp.read())
    fp.close()

    msg["Subject"] = "Issue with exporting complete ILINett text file"
    msg["From"] = "bernice.boursiquot@ihs.gov"
    msg["To"] = "bernice.boursiquot@ihs.gov"

    s = smtplib.SMTP("localhost")
    s.sendmail("bernice.boursiquot@ihs.gov","bernice.boursiquot@ihs.gov", msg.as_string())
    s.quit()	
   