#!/usr/bin/env python
# coding: utf-8

# #Libraries and Data

# In[30]:


#import libraries
import numpy as np
import pandas as pd
import itertools
from prophet import Prophet
import yfinance
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


# In[32]:


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
    


# In[33]:


#symbols = ["OLECTRA.NS","LT.NS","CONCOR.NS","ELGIEQUIP.NS","IOC.NS","BEL.NS","TATAELXSI.NS","^NSEI"]
symbols = ["OLECTRA.NS","CONCOR.NS","ELGIEQUIP.NS","IOC.NS","BEL.NS","TATAELXSI.NS","^NSEI","HDFCBANK.NS","TATAMOTORS.NS","SBIN.NS","TCS.NS","TITAN.NS","SUNPHARMA.BO","TECHM.NS", "ASIANPAINT.NS","TATACONSUM.NS"]
#symbols = ["RELI","HDFCBANK.NS"]
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
#stock_data = fetch_stock_data(symbols)
finaldata = {}
current_date = datetime.now().strftime("%d-%m-%Y")

for symbol in symbols:
    stock_name = symbol
    if symbol == "^NSEI":
        stock_name = "NSEI"
 
    data = load_and_setup_data(symbol)
    # data.to_csv(f"../stock_historical_data/{symbol}.csv")
    #data = DataProcessing(symbol,data)
    # Specify Target
    # data.df.loc[data.df["Range"].shift(-1) > data.df["Avg_Range"], "TARGET"] = 1
    # data.df.loc[data.df["Range"].shift(-1) <= data.df["Avg_Range"], "TARGET"] = 0
    loaded_model = {}
    loaded_model_prophet = {}

    #feature_item = {}
    with open('../TrainedModel/xg/{}_model_phrophet.pkl'.format(symbol), 'rb') as f:
        loaded_model_prophet = pickle.load(f)
    with open('../TrainedModel/xg/{}_model_2.pkl'.format(symbol), 'rb') as f:
        loaded_model = pickle.load(f)
   # with open('../TrainedModel/xg/{}_features.txt'.format(symbol), 'rb') as f:
    #    feature_item = pickle.load(f)
    #final training
    loaded_models[symbol] = loaded_model
    data  = add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
    data = data.dropna()
    data["ds"] = data.index
   # data["Date"] =  pd.to_datetime(data['Date'])
    data["y"] = data["Close"]

    print(data)
    forecast = loaded_model_prophet.predict(data)
    data = data.reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='')
    
    #data = data.drop("index",axis=1)
    
    #get some variables
    prophet_variables = forecast.loc[:, ["trend", "weekly",  "multiplicative_terms","trend_upper","trend_lower"]]
    df_xgb = pd.concat([data, prophet_variables], axis = 1)
    non_stationaries = []
    for col in df_xgb.columns:
        if col != "multiplicative_terms" and col != "Date" and col != "ds" :
            #print(col)
            dftest = adfuller(df_xgb[col].values)
            p_value = dftest[1]
            t_test = dftest[0] < dftest[4]["1%"]
            if p_value > 0.05 or not t_test:
                non_stationaries.append(col)
    #print(f"Non-Stationary Features Found: {len(non_stationaries)}")
    
    df_stationary = df_xgb.copy()

    df_stationary = df_stationary.drop(columns=["Date","ds"])
    df_stationary[non_stationaries] = df_stationary[non_stationaries].pct_change()
    #print(df_stationary)
    df_stationary = df_stationary[loaded_model.feature_names_in_]

   # score = loaded_model.predict(df_stationary)
    y_train_pred = loaded_model.predict_proba(df_stationary)[:,1]
    
    #print(y_train_pred)
        #df_xgb.head(1)
    #print(forecast)
   # final_target[symbol] = data.df["TARGET"]
   # df = data.df[feature_item]
   # finaldata[symbol]= df 
    stock_name_only = stock_name.replace(".NS","")
    train_yhat = loaded_model.predict(df_stationary[-1:])
    train_yhat_proba = loaded_model.predict_proba(df_stationary[-1:])
    greater = 0
    one = train_yhat_proba[0][0]
    two = train_yhat_proba[0][1]
    if one > two:
        greater = one*100
    else:
        greater = one*100
   # print(greater)
    #final_result[symbol] = [current_date,train_yhat[0],1,'xg',stock_name_only,stock_data.head(1).Close[symbol].values[0],round(greater,2)]
    result.append([current_date,train_yhat[0],1,'xg',stock_name_only,data.iloc[-1].Close,round(greater,2)])

#print(result)
    


# In[34]:


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


# In[35]:


import requests
import json

url = "https://website-development-kerala.com/api_214124524/ai_model_daily_runner.php"

response = requests.post(url, json=dataa)
print(response.status_code)
print(response)


# In[36]:


final_target


# In[9]:


#for symbol in symbols:
   # retrained_model = loaded_models[symbol].fit(finaldata[symbol],final_target[symbol])
    #print(retrained_model)
    #with open('../TrainedModel/xg/{}_model_2.pkl'.format(symbol), 'wb') as f:
     #   pickle.dump(retrained_model, f)

