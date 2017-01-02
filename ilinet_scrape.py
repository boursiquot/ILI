#import requests
import urllib2 as url
import pandas as pd
from bs4 import BeautifulSoup as bs
from lxml import html 

site = "https://www.cdc.gov/flu/weekly/weeklyarchives2016-2017/data/senAllregt50.html"

page = url.urlopen(site)

soup = bs(page,"html.parser")

table_headers = soup.findAll("tr",limit = 2)[0].findAll("th")

#print table_headers 

column_headers = [th.getText() for th in soup.findAll("tr",limit = 2)[0].findAll("th")]

#print column_headers,type(column_headers)

data_rows = soup.findAll("tr")[1:]

#print data_rows,type(data_rows)

ili_data = [[td.getText() for td in data_rows[i].findAll("td")] for i in range(len(data_rows))]

ili_data2  = pd.to_numeric(ili_data) 
print ili_data2

#df = pd.DataFrame(ili_data, columns = column_headers)

#df = df.convert_objects(convert_numeric = True)

#df = pd.to_numeric(df)

#print df.dtypes

#df.loc[:,"Week"] = df.loc[:,"Week"].astype(str)
#print  df
