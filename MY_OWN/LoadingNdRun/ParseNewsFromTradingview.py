#!/usr/bin/env python
# coding: utf-8

# In[56]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
def scrape_website(url):
    # Send an HTTP GET request to the website
    response = requests.get(url)
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Check if the request was successful
    if response.status_code == 200:
        result = []
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        a_links = soup.find_all('a')
        
        for x in a_links:
            temp_res = {}
            if x.get('target') == "_blank" and x.get('href').split("/")[1] == "news":
                timDom = x.find("relative-time")
                timeSpliter = timDom.text.strip().split(" ")
                timeSpliterFlag = False
                for tim in timeSpliter:
                    if tim == "hours" or tim == "hour" or tim == "minutes" or tim == "minute":
                        timeSpliterFlag = True;
                        
                if timeSpliterFlag == False:
                    break
                
                article_main = x.find('article')
                #article_main_div = article_main.find('div')
                temp_stocks = []
                stocks_dom = article_main.find_all('img')
                if len(stocks_dom) != 0:
                    for c in stocks_dom:
                        imgSecArr = c.get('src').split("/")
                        imgCurrent = imgSecArr[len(imgSecArr)-1]
                        exactURL = imgCurrent.split(".")
                        #print(exactURL)
                        if exactURL[1] == "svg":
                            temp_stocks.append(exactURL[0])
                temp_res["stocks"] = json.dumps(temp_stocks)         
                article_main_span = article_main.find_all('span')
                temp_res["content"]  = article_main_span[len(article_main_span)-1].text.strip()
                temp_res["date"]  = timDom.get("event-time")
                result.append(temp_res)
                
        return result
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")

    return None

# URL of the website from which you want to scrape data
target_url = 'https://in.tradingview.com/markets/stocks-india/news/'

# Fetch FII and DII data from the website
data = scrape_website(target_url)

# Display the extracted data
print(data)


# In[58]:


dataa = { "data":[]} 


dataa["data"] = data
dataa


# In[59]:


import requests
import json

url = " https://smarttradersclub.in/api_214124524/oi_news.php"

response = requests.post(url, json=dataa)
print(response.status_code)
print(response)

