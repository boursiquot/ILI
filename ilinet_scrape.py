#import requests 
import urllib2 as url
from bs4 import BeautifulSoup as bs

site = "https://www.cdc.gov/flu/weekly/weeklyarchives2016-2017/data/senAllregt50.html"

page = url.urlopen(site)

soup = bs(page,"html.parser")

#print soup.prettify()

#print soup.title.string

table_headers = soup.find_all("th")

print type(table_headers)

#ili_data = soup.find_all("td")

#print ili_data
