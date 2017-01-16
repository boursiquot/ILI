#import requests
import urllib2 as url
import pandas as pd
from bs4 import BeautifulSoup as bs
from lxml import html

site = "https://www.cdc.gov/flu/weekly/weeklyarchives2016-2017/data/senAllregt01.html"

page = url.urlopen(site)

soup = bs(page,"html.parser")

table_headers = soup.findAll("tr",limit = 2)[0].findAll("th")

column_headers = [th.getText() for th in soup.findAll("tr",limit = 2)[0].findAll("th")]

column_headers.insert(0,"Region Type")

column_headers.insert(1,"Region")

column_headers.insert(2,"Year")

print column_headers

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

print ili_data    

df  = pd.DataFrame(ili_data, columns = column_headers)

#df = df.apply(pd.to_numeric)

print df

#df.loc[:,"Week"] = df.loc[:,"Week"].astype(str)
#print  df
