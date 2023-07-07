#!/usr/bin/env python
# coding: utf-8

# #Libraries and Data

# In[10]:


#import libraries
import numpy as np
import pandas as pd
import itertools
from prophet import Prophet
import yfinance
import pickle
import xgboost as xgb
from datetime import datetime


# In[11]:


def fbprobetModel(stock_name,input_data):
    # Load the saved model from the file
    loaded_model = {}
    with open('../TrainedModel/prophet/{}_prophet_model_1.pkl'.format(stock_name), 'rb') as f:
        loaded_model = pickle.load(f)
    
    # Load the saved model from the file
    loaded_model_prophet = {}
    with open('../TrainedModel/prophet/{}prophet_model_2.pkl'.format(stock_name), 'rb') as f:
        loaded_model_prophet = pickle.load(f)
    
    data = {
    'ds' : [input_data["ds"]]
     }
  

    # Create a new DataFrame object
    data_fr = pd.DataFrame(data)
    data_fr.head()
    
    forecast = loaded_model_prophet.predict(data_fr)
    
    #get some variables
    df_xgb = forecast.loc[:, ["trend", "weekly",  "multiplicative_terms","yhat"]]
    # Create a dictionary with data
    data = {
     #   'Open': [input_data["Open"]],

        'High': [input_data["High"]],
        'Low': [input_data["Low"]],
        'y': [input_data["Close"]],
        'Volume': [input_data["Volume"]],
        'trend': df_xgb.head(1).trend.values,
        'weekly':df_xgb.head(1).weekly.values,
        'multiplicative_terms': df_xgb.head(1).multiplicative_terms.values,
    }
    print("point 1",data)


    # Create a new DataFrame object
    df = pd.DataFrame(data)
    print("point 2",df.head())

    Future = xgb.DMatrix(df, label = df.y)
    print("point 3",df)

    f_predictions = pd.Series(loaded_model.predict(Future), name = "XGBoost")
    return f_predictions


# In[12]:


def fetch_stock_data(tickers):
    data = yfinance.download(tickers,period='1d')
    return data


# In[13]:


tickers = ["OLECTRA.NS","LT.NS","CONCOR.NS","ELGIEQUIP.NS","IOC.NS","BEL.NS","TATAELXSI.NS","^NSEI"]
  # Add the tickers you want to fetch data for
stock_data = fetch_stock_data(tickers)


# In[5]:


stock_data


# In[16]:


result = []
Icdate = 0
Iresult = 1
IisClassification = 2
Imodel = 3
Istock = 4
Iclose = 5

current_date = datetime.now().strftime("%d-%m-%Y")

for ticker in tickers:
    stock_name = ticker
    if ticker == "^NSEI":
        stock_name = "NSEI"
        
    input_data = {
                    # "Open" : stock_data.head(1).Open[ticker].values[0],

                    "Close" : stock_data.head(1).High[ticker].values[0],
                    "High" : stock_data.head(1).High[ticker].values[0],
                    "Low" : stock_data.head(1).Low[ticker].values[0], 
                    "Volume" : stock_data.head(1).Volume[ticker].values[0],
                    "ds":np.datetime_as_string(stock_data.index, unit='D')[0]
                }
    
   
    stock_name_only = stock_name.replace(".NS","")
    print(stock_name_only)
    print(input_data)

        
    model_result  = fbprobetModel(stock_name_only,input_data)
    print(model_result)
    result.append([current_date,model_result[0],0,'prophet',stock_name_only,stock_data.head(1).Close[ticker].values[0]])


# In[19]:


dataa = { "data":[]} 

for res in result:
    dataa["data"].append({ 
            "cdate": res[Icdate],
            "result": str(res[Iresult]),
            "pre_close" : str(res[Iclose]),            
            "isClassification": res[IisClassification],
            "model": res[Imodel],
            "prob": "0",
            "stock": res[Istock]})
    
dataa


# In[20]:


import requests
import json

url = "https://website-development-kerala.com/api_214124524/ai_model_daily_runner.php"

response = requests.post(url, json=dataa)
print(response.status_code)
print(response)

