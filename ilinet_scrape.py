#import requests
 import urllib2 as url

from bs4 import BeautifulSoup as bs
from lxml import html 

site = "https://www.cdc.gov/flu/weekly/weeklyarchives2016-2017/data/senAllregt50.html"

page = url.urlopen(site)

soup = bs(page,"html.parser")

right_table  = soup.find_all("table")
#print all_tables #print soup.prettify() 
#print soup.title.string

table_headers = soup.findAll("tr",limit = 2)

print table_headers 

ili_data = soup.find_all("td")
    #for row in right_table.findAll("tr"):
#    cell = row.findAll("td")
#    headers = row.findAll("th") 
    

    
