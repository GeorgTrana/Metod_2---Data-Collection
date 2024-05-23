#%%
import urllib.request
import requests
from bs4 import BeautifulSoup
import time
import numpy as np 
import pandas as pd
import os
#%%


#links
base_url = 'https://gupea.ub.gu.se'

url_2018 = 'https://gupea.ub.gu.se/handle/2077/543/discover?filtertype_1=dateIssued&filter_relational_operator_1=contains&filter_1=2018&submit_apply_filter=&query=&rpp=50&sort_by=score&order=desc'
url_2019 = 'https://gupea.ub.gu.se/handle/2077/543/discover?filtertype_1=dateIssued&filter_relational_operator_1=contains&filter_1=2019&submit_apply_filter=&query=&rpp=50&sort_by=score&order=desc'
url_2020 = 'https://gupea.ub.gu.se/handle/2077/543/discover?filtertype_1=dateIssued&filter_relational_operator_1=contains&filter_1=2020&submit_apply_filter=&query=&rpp=50&sort_by=score&order=desc'
url_2021 = 'https://gupea.ub.gu.se/handle/2077/543/discover?filtertype_1=dateIssued&filter_relational_operator_1=contains&filter_1=2021&submit_apply_filter=&query=&rpp=50&sort_by=score&order=desc'
url_2022 = 'https://gupea.ub.gu.se/handle/2077/543/discover?filtertype_1=dateIssued&filter_relational_operator_1=contains&filter_1=2022&submit_apply_filter=&query=&rpp=50&sort_by=score&order=desc'
url_2023 = 'https://gupea.ub.gu.se/handle/2077/543/discover?filtertype_1=dateIssued&filter_relational_operator_1=contains&filter_1=2023&submit_apply_filter=&query=&rpp=50&sort_by=score&order=desc'

l_pre_cov = []
l_dur_cov = []
l_aft_cov = []

#For later categorizing
years = {
    #url_2018 : l_pre_cov,
    #url_2019 : l_pre_cov,
    url_2020 : l_dur_cov ,
    url_2021 : l_dur_cov ,
    url_2022 : l_aft_cov,
    url_2023 : l_aft_cov
    }

for url in years:
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    links = soup.find_all(class_='image-link') #Link found in
   
    l_href = []
    for link in links:
        href = link.get('href')
        l_href.append(href)

    for href in l_href:
        url2 = f"https://gupea.ub.gu.se{href}"
        req = requests.get(url2)
        soup = BeautifulSoup(req.text, 'html.parser')
        for link in soup.find_all("a"):
            href = link.get('href',[]) #Links found in
            text = link.get_text() #Word "Abstract" found in
            if ('.pdf' in href):
                if ('Abstract' in text):
                    years[url].append(f"{base_url}{href}")    #{text} |{href}")
                elif ('ABSTRACT' in text):
                    years[url].append(f"{base_url}{href}")
                elif ('Spikblad' in text):
                    years[url].append(f"{base_url}{href}")
                elif ('SPIKBLAD' in text):
                    years[url].append(f"{base_url}{href}")
        
        print(len(years[url]))


for nr,pdf_link in enumerate(l_pre_cov):
    local_path = f"./pre_cov/{nr}_pre_cov.pdf"
    urllib.request.urlretrieve(pdf_link, local_path)
    
for nr,pdf_link in enumerate(l_dur_cov):
    print(pdf_link)
    local_path = f"./dur_cov/{nr}_dur_cov.pdf"
    urllib.request.urlretrieve(pdf_link, local_path)
    
for nr,pdf_link in enumerate(l_aft_cov):
    local_path = f"./aft_cov/{nr}_aft_cov.pdf"
    urllib.request.urlretrieve(pdf_link, local_path)
    
    
    
    
    
    
