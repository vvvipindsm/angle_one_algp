#!/usr/bin/env python
# coding: utf-8

# In[22]:


import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send an HTTP GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        result = {}
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the tables containing FII and DII data (update the class names as per the website)
        fii_table = soup.find_all('table', class_='mctable1 tble1')
        fii_table_t_body = fii_table[0].find('tbody')
        fii_table_body_tr = fii_table_t_body.find('tr')
        fii_table_body_tr_td = fii_table_t_body.find_all('td')[1]
    

        fii_table_body_date = fii_table_body_tr.find('span', class_='desk-hide').text.strip()
        result["fii_purchase"] = fii_table_body_tr_td.text.strip()
        result["fii_sell"] = fii_table_t_body.find_all('td')[2].text.strip()
        result["fii_gross"] = fii_table_t_body.find_all('td')[3].text.strip()
        
        result["dii_purchase"] =fii_table_t_body.find_all('td')[4].text.strip()
        result["dii_sell"] = fii_table_t_body.find_all('td')[5].text.strip()
        result["dii_gross"] = fii_table_t_body.find_all('td')[6].text.strip()


        result["date"] = fii_table_body_date

        print(fii_table_body_tr_td.text.strip())
        return result
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")

    return None

# URL of the website from which you want to scrape data
target_url = 'https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php'

# Fetch FII and DII data from the website
data = scrape_website(target_url)

# Display the extracted data
print(data)


# In[27]:


import requests
import json

url = "https://website-development-kerala.com/api_214124524/fii_runner.php"

response = requests.post(url, json=data)
print(response.status_code)
print(response)

