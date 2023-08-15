#!/usr/bin/env python
# coding: utf-8

# In[58]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_website(url):
    # Send an HTTP GET request to the website
    response = requests.get(url)
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Check if the request was successful
    if response.status_code == 200:
        result = {}
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        o_t = soup.find_all('table')[0]
        op_t_tbody = o_t.find('tbody')
        op_t_tbody_trs = op_t_tbody.find_all('tr')
        result = []
        for x in range(len(op_t_tbody_trs)-1):
            print(x)
            temp = {}
            if x < 53:
                
                tr = op_t_tbody_trs[x]
                tds = tr.find_all('td')
                #stike price
                strike = tds[3]
                strike_div = strike.find('div')
                strike_inner_div = strike_div.find('div')

                temp["strike"] = strike_inner_div.text.strip()
                #call price
                call_pr = tds[2]
                call_a = call_pr.find('a')
                temp["call_price"] = call_a.text.strip()
                temp["date"] = current_date

                #put price 
                put_pr = tds[4]
                put_a = put_pr.find('a')
                temp["put_price"] = put_a.text.strip()
                #oi
                divs = tds[1].find_all("div")
                innerDiv = divs[1].find("div")
                innerDiv1 = innerDiv.find_all("div")

                temp["oi"] = innerDiv1[0].text.strip()
                temp["oi_p"] = innerDiv1[1].text.strip()
                #oi call
                divs = tds[5].find_all("div")
                innerDiv = divs[1].find("div")
                innerDiv1 = innerDiv.find_all("div")

                print(innerDiv)
                temp["oi_call"] = innerDiv1[0].text.strip()
                temp["oi_call_p"] = innerDiv1[1].text.strip()
            if (len(temp.keys()) > 0):
                result.append(temp)
        return result
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")

    return None

# URL of the website from which you want to scrape data
target_url = 'https://groww.in/options/nifty'

# Fetch FII and DII data from the website
data = scrape_website(target_url)

# Display the extracted data
print(data)


# In[61]:


dataa = { "data":[]} 


dataa["data"] = data


# In[62]:


import requests
import json

url = "https://smarttradersclub.in/api_214124524/oi_runner.php"

#response = requests.post(url, json=dataa)
#print(response.status_code)
#print(response)

