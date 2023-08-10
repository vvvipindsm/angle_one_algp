#!/usr/bin/env python
# coding: utf-8

# #Libraries and Data

# In[7]:


#import libraries
import numpy as np
import pandas as pd
import itertools
from prophet import Prophet
import yfinance
import json

import pickle
from statsmodels.tsa.stattools import adfuller

import xgboost as xgb
from datetime import datetime

from dataProcessing import DataProcessing
# Remove Future Warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from ta import add_all_ta_features




from sklearn.model_selection import train_test_split

# Machine Learning
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

# Evaluation
from sklearn.metrics import precision_score

# Reporting
import matplotlib.pyplot as plt


# In[9]:


def load_and_setup_data(sybmol):
    df = pd.read_csv("../stock_historical_data/{}.csv".format(sybmol))
    df.set_index("Date", inplace=True)
    #new_data = pd.DataFrame(input_data)
   # new_data.set_index("Date", inplace=True)
  #  concatenated_df = pd.concat([df,new_data])
   # print(concatenated_df)
    #print(concatenated_df)
    return df

def fetch_stock_data(tickers):
    data = yfinance.download(tickers,period='1d')
    #print(data)
    return data
def exponential_moving_average(data, window):
    if len(data) < window:
        raise ValueError("Data length should be greater than or equal to the window size.")
    
    alpha = 2 / (window + 1)
    ema = [data[0]]

    for i in range(1, len(data)):
        ema_value = alpha * data[i] + (1 - alpha) * ema[-1]
        ema.append(ema_value)
    return ema
    


# In[10]:


#symbols = ["OLECTRA.NS","LT.NS","CONCOR.NS","ELGIEQUIP.NS","IOC.NS","BEL.NS","TATAELXSI.NS","^NSEI"]
#symbols = ["OLECTRA.NS","CONCOR.NS","ELGIEQUIP.NS","IOC.NS","BEL.NS","TATAELXSI.NS","^NSEI","HDFCBANK.NS","TATAMOTORS.NS","SBIN.NS","TCS.NS","TITAN.NS","SUNPHARMA.BO","TECHM.NS", "ASIANPAINT.NS","TATACONSUM.NS"]
#symbols = ["OLECTRA.NS","CONCOR.NS",]
#symbols =  ["INR=X","^DJI","^DJI","^FTSE","BTC-USD","^VIX","RTY=F"]

symbols = [ "^NSEI","^NSEBANK" , "^CNXFMCG","NIFTY_FIN_SERVICE.NS","^CNXIT","NIFTY_PVT_BANK.NS","^CNXMETAL"]

Icdate = 0
Iresult = 1
IisClassification = 2
Imodel = 3
Istock = 4
Iclose = 5
Iprob = 6
Ichange = 7

  # Add the tickers you want to fetch data for
loaded_models = {}
result = []

final_result = {}
final_target = {}
#stock_data = fetch_stock_data(symbols)
finaldata = {}
current_date = datetime.now().strftime("%d-%m-%Y")

for symbol in symbols:
    stock_name = symbol
    if symbol == "^NSEI":
        stock_name = "NSEI"
    print(stock_name)
    data = load_and_setup_data(symbol)
    #moving av
    data['MA5'] = data.Close.rolling(window=5).mean()
    data['EMA5'] = exponential_moving_average(data.Close.values,5)

    data['MA10'] = data.Close.rolling(window=50).mean()
    data['EMA10'] = exponential_moving_average(data.Close.values,10)

    data['MA20'] = data.Close.rolling(window=20).mean()
    data['EMA20'] = exponential_moving_average(data.Close.values,20)

    data['MA50'] = data.Close.rolling(window=50).mean()
    data['EMA50'] = exponential_moving_average(data.Close.values,50)

    data['MA100'] = data.Close.rolling(window=100).mean()
    data['EMA100'] = exponential_moving_average(data.Close.values,100)

    data.dropna(inplace=True)
    loaded_model_prophet = {}

    with open('../TrainedModel/fp_tech_indicator/{}.pkl'.format(symbol), 'rb') as f:
        loaded_model_prophet = pickle.load(f)
        
    data["ds"] = data.index
    data["y"] = data["Close"]
    data = data.reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='')

    forecast = loaded_model_prophet.predict(data)
    forecast["Close"] =  data['y'].values
    change = forecast["Close"].iloc[-1] - forecast["Close"].iloc[-2]

    forecast["yearly"] = 0
    forecast["weekly"] = 0
    forecast["ma20above50"] = 0
    forecast["ma50above100"] = 0
    forecast["ma20above100"] = 0
    forecast["ma5"] = 0
    forecast["ma10"] = 0
    forecast["ma20"] = 0
    forecast["ma50"] = 0
    forecast["ma100"] = 0
    forecast["ema5"] = 0
    forecast["ema10"] = 0
    forecast["ema20"] = 0
    forecast["ema50"] = 0
    forecast["ema100"] = 0
    forecast["TARGET"] = 0
    
    forecast["MA20"] =  data['MA20'].values
    forecast["MA100"] =  data['MA100'].values
    forecast["MA50"] =  data['MA50'].values
    forecast["MA5"] =  data['MA5'].values
    forecast["MA10"] =  data['MA10'].values

    forecast["EMA20"] =  data['EMA20'].values
    forecast["EMA100"] =  data['EMA100'].values
    forecast["EMA50"] =  data['EMA50'].values
    forecast["EMA5"] =  data['EMA5'].values
    forecast["EMA10"] =  data['EMA10'].values
    forecast.loc[forecast["Close"].shift(-1) > forecast["Close"],"TARGET"] = 1

    forecast.loc[forecast["MA5"] < forecast["Close"],"ma5"] = 1
    forecast.loc[forecast["EMA5"] < forecast["Close"],"ema5"] = 1

    forecast.loc[forecast["MA10"] < forecast["Close"],"ema10"] = 1
    forecast.loc[forecast["EMA10"] < forecast["Close"],"ema10"] = 1


    forecast.loc[forecast["MA20"] < forecast["Close"],"ema20"] = 1
    forecast.loc[forecast["EMA20"] < forecast["Close"],"ema20"] = 1

    forecast.loc[forecast["MA50"] < forecast["Close"],"ema50"] = 1
    forecast.loc[forecast["EMA50"] < forecast["Close"],"ema50"] = 1

    forecast.loc[forecast["MA100"] < forecast["Close"],"ema100"] = 1
    forecast.loc[forecast["EMA100"] < forecast["Close"],"ema100"] = 1
    #forecast.loc[forecast["yearly"].shift(-1) > forecast["yearly"],"yearly"] = 1

    #forecast.loc[forecast["weekly"].shift(-1) > forecast["weekly"],"weekly"] = 1
    forecast.loc[forecast["trend"].shift(1) < forecast["trend"],"trend"] = 1

    forecast.loc[forecast["MA20"] > forecast["MA50"],'ma20above50'] = 1
    forecast.loc[forecast["MA50"] > forecast["MA100"],'ma50above100'] = 1
    forecast.loc[forecast["MA20"] > forecast["MA100"],'ma20above100'] = 1

    forecast.dropna(inplace=True)
    new_df1 = forecast[["trend","ma20above50","ma50above100","ma20above100","ma5","ma20","ma50","ma100","ema5","ema10","ema20","ema50","ema100"]]

    c_df = new_df1.iloc[-1]
    dd =  c_df.to_dict()
  
    stock_name_only = stock_name.replace(".NS","")
    result.append([current_date,json.dumps(dd),1,'indicator_list_nifty',stock_name_only,data.iloc[-1].Close,50,change])

print(result)
    


# In[11]:


dataa = { "data":[]} 

for res in result:
    dataa["data"].append({ 
            "cdate": res[Icdate],
            "result": str(res[Iresult]),
            "pre_close" : str(res[Iclose]),            
            "isClassification": res[IisClassification],
            "model": res[Imodel],
            "stock": res[Istock],
            "prob": str(res[Iprob]),
            "change" : res[Ichange],
    })
    
dataa


# In[36]:


import requests
import json

url = "https://website-development-kerala.com/api_214124524/ai_model_daily_runner.php"

response = requests.post(url, json=dataa)
print(response.status_code)
print(response)

