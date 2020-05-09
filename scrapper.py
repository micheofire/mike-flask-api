#Import necessary libries
import requests, re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re

#empty list
l = []


#base url of the website
base_url = "https://www.cheki.com.ng/vehicles?"

#using request and beautiful soup
r = requests.get(base_url)
c = r.content
soup = BeautifulSoup(c, "html.parser")

#get the total pages to scrape
n_items = int(soup.find("div", {"class":"gridsortby"}).text.split()[0])
listings = 20
page_nr = int(np.round(n_items/listings))


#scrape each page in a loop
for page in range(1,int(page_nr),1):
    r=requests.get(base_url+"?page="+str(page))
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    content = soup.find_all("div", {"class":"middle-right-footer-wrapper"})
    
    #iterate over contents
    for i in list(range(0,len(content))):
        d = {}
        try:
            d["desc"] = content[i].find_all("span", {"class":"ellipses"})[1].text.strip().replace("\n", " ")
        except (IndexError,TypeError,AttributeError) as e:
            d["desc"] = None
        try:
            d["trans"] = re.findall("Automatic", content[i].find_all("ul", {"class":"card-features"})[0].text.strip())[0].lower()
        except (IndexError,TypeError,AttributeError) as e:
            d["trans"] = "manual"
        try:
            d["origin"] = re.findall("Foreign", content[i].find_all("ul", {"class":"card-features"})[0].text.strip())[0].lower()
        except (IndexError,TypeError,AttributeError) as e:
            d["origin"]= "local"
        try:
            d["engine"] = re.findall("Petrol", content[i].find_all("ul", {"class":"card-features"})[0].text.strip())[0].lower()
        except (IndexError,TypeError,AttributeError) as e:
            d["engine"] = "diesel"
#         try:
#             d["year"] = int(re.findall("20..", content[i].find_all("ul", {"class":"card-features"})[0].text.strip())[0])
#         except (IndexError,TypeError,AttributeError) as e:
#             d["year"] = 1990
        try:
            d["price"] = int(content[i].find("h2", {"class":"listing-price"}).text.strip().replace("₦", "").replace(",", ""))
        except (IndexError,TypeError,AttributeError) as e:
            d["price"] = None
            
        #append the dictionary to a list
        l.append(d)
        
        
#convert list to dataframe        
ld = pd.DataFrame(l)


#convert to csv
ld.to_csv('cheki1.csv')