import urllib2 as url
import pandas as pd
from bs4 import BeautifulSoup as bs
from lxml import html
import datetime as dt
import logging as lg
import sys

start = dt.datetime.now().strftime("%Y/%m/%d %H:%M")

date = dt.date.today().strftime("%Y%m%d")

logname = "/Users/bernice/GitHub/ILI/logs/ilinet" + date + ".log"

lg.basicConfig(filename=logname,level=lg.INFO,filemode = "w")

lg.info ("ILI Net data checked at {0}.".format(start))

week = dt.date.today().isocalendar()[1] 

## NEED TO CHECK WEEK FOR LENGTH 

week = "0" + str(week-2) ##01-17-2017: change -2 to -1; is currently -1 for testing errors and logs

site = "https://www.cdc.gov/flu/weekly/weeklyarchives2016-2017/data/senAllregt" + week + ".html"

try:

    page = url.urlopen(site)

except url.HTTPError as err:

    lg.error(err) 
    print "Error occurred; check log"
    sys.exit(1) ## From Python docs: a zero value is considered to be a sucessful termination
                ## A non-zero value is considered to be an abnormal termination

soup = bs(page,"html.parser")

table_headers = soup.findAll("tr",limit = 2)[0].findAll("th")

column_headers = [th.getText() for th in soup.findAll("tr",limit = 2)[0].findAll("th")]

column_headers.insert(0,"Region Type")

column_headers.insert(1,"Region")

column_headers.insert(2,"Year")

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

df  = pd.DataFrame(ili_data, columns = column_headers)

#print df

filename = "/Users/bernice/Github/ILI/output/_ILINett - " + date + ".txt"

try:

    df.to_csv(filename, sep=',')
    lg.info("ILI Net data were sucessfully scraped and exported")

except:

    lg.info("Issue with scraping and exporting data")
