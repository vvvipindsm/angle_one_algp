#!/usr/bin/env python
# coding: utf-8

# #Libraries and Data

# In[1]:


#import libraries
import numpy as np
import pandas as pd
import itertools
from prophet import Prophet
import yfinance
import pickle
import xgboost as xgb
from datetime import datetime

from dataProcessing import DataProcessing
# Remove Future Warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)




from sklearn.model_selection import train_test_split

# Machine Learning
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

# Evaluation
from sklearn.metrics import precision_score

# Reporting
import matplotlib.pyplot as plt


# In[2]:


def load_and_setup_data(sybmol,input_data):
    df = pd.read_csv("../stock_historical_data/{}.csv".format(sybmol))
    df.set_index("Date", inplace=True)
    new_data = pd.DataFrame(input_data)
    new_data.set_index("Date", inplace=True)
    concatenated_df = pd.concat([df,new_data])
    return concatenated_df

def fetch_stock_data(tickers):
    data = yfinance.download(tickers,period='1d')
    print(data)
    return data
    


# In[4]:


symbols = ["OLECTRA.NS","LT.NS","CONCOR.NS","ELGIEQUIP.NS","IOC.NS","BEL.NS","TATAELXSI.NS","^NSEI"]

Icdate = 0
Iresult = 1
IisClassification = 2
Imodel = 3
Istock = 4
Iclose = 5
Iprob = 6
  # Add the tickers you want to fetch data for
loaded_models = {}
result = []

final_result = {}
final_target = {}
stock_data = fetch_stock_data(symbols)
print(stock_data)
finaldata = {}
current_date = datetime.now().strftime("%d-%m-%Y")

for symbol in symbols:
    stock_name = symbol
    if symbol == "^NSEI":
        stock_name = "NSEI"
 
    input_data = {
                    # "Open" : stock_data.head(1).Open[ticker].values[0],
                    "Open" : [stock_data.head(1).Open[symbol].values[0]],
                    "Close" : [stock_data.head(1).Close[symbol].values[0]],
                    "High" : [stock_data.head(1).High[symbol].values[0]],
                    "Low" : [stock_data.head(1).Low[symbol].values[0]], 
                    "Volume" : [stock_data.head(1).Volume[symbol].values[0]],
                    "Date":[np.datetime_as_string(stock_data.index, unit='D')[0]]
    }
    print(input_data)
    data = load_and_setup_data(symbol,input_data)
    data.to_csv(f"../stock_historical_data/{symbol}.csv")
    data = DataProcessing(symbol,data)
    # Specify Target
    data.df.loc[data.df["Range"].shift(-1) > data.df["Avg_Range"], "TARGET"] = 1
    data.df.loc[data.df["Range"].shift(-1) <= data.df["Avg_Range"], "TARGET"] = 0
    loaded_model = {}
    feature_item = {}
    with open('../TrainedModel/xg/{}_model_2.pkl'.format(symbol), 'rb') as f:
        loaded_model = pickle.load(f)
    with open('../TrainedModel/xg/{}_features.txt'.format(symbol), 'rb') as f:
        feature_item = pickle.load(f)
    #final training
    loaded_models[symbol] = loaded_model
    data.df = data.df.dropna()

    final_target[symbol] = data.df["TARGET"]
    df = data.df[feature_item]
    finaldata[symbol]= df 
    stock_name_only = stock_name.replace(".NS","")
    train_yhat = loaded_model.predict(df[-1:])
    train_yhat_proba = loaded_model.predict_proba(df[-1:])
    greater = 0
    one = train_yhat_proba[0][0]
    two = train_yhat_proba[0][1]
    if one > two:
        greater = one*100
    else:
        greater = one*100
#    print(greater)
    final_result[symbol] = [current_date,train_yhat[0],1,'xg',stock_name_only,stock_data.head(1).Close[symbol].values[0],round(greater,2)]
    result.append([current_date,train_yhat[0],1,'xg',stock_name_only,stock_data.head(1).Close[symbol].values[0],round(greater,2)])

print(result)


# In[7]:


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
    })
    
dataa


# In[8]:


import requests
import json

url = "https://website-development-kerala.com/api_214124524/ai_model_daily_runner.php"

response = requests.post(url, json=dataa)
print(response.status_code)
print(response)


# In[9]:


final_target


# In[10]:


for symbol in symbols:
    retrained_model = loaded_models[symbol].fit(finaldata[symbol],final_target[symbol])
    print(retrained_model)
    with open('../TrainedModel/xg/{}_model_2.pkl'.format(symbol), 'wb') as f:
        pickle.dump(retrained_model, f)

