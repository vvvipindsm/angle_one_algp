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
from ta import add_all_ta_features

from dataProcessing import DataProcessing
# Remove Future Warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from statsmodels.tsa.stattools import adfuller
from sklearn.preprocessing import StandardScaler




from sklearn.model_selection import train_test_split

# Machine Learning
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

# Evaluation
from sklearn.metrics import precision_score

# Reporting
import matplotlib.pyplot as plt


# In[17]:


def load_and_setup_data(sybmol,input_data):
    df = pd.read_csv("../stock_historical_data/{}.csv".format(sybmol))
  #  df.set_index("Date", inplace=True)
    new_data = pd.DataFrame(input_data)
    new_data.set_index("Date", inplace=True)
    #concatenated_df = pd.concat([df,new_data])
    return df

def fetch_stock_data(tickers):
    data = yfinance.download(tickers,period='1d')
    return data
    


# In[47]:


#symbols = ["CONCOR.NS","ELGIEQUIP.NS"]
symbols = ["OLECTRA.NS","CONCOR.NS","ELGIEQUIP.NS","IOC.NS","BEL.NS","TATAELXSI.NS","^NSEI"]


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
#print(stock_data)
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
    #print(input_data)
    data = load_and_setup_data(symbol,input_data)
    data = data[["Open", "High", "Low", "Close","Volume"]]

   # data.to_csv(f"../stock_historical_data/{symbol}.csv")
    data = add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
    # Find NaN Rows
    #na_list = data.columns[data.isna().any().tolist()]
   # data.drop(columns=na_list, inplace=True)
    # Handle inf values
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.dropna(axis=1, inplace=True)
    #data = data.drop(['volatility_kchi','volatility_kcli'], axis=1)

    #df_stationary.head()
   # print(data)
    non_stationaries = []
    for col in data.columns:
        if col != "volatility_kchi" and col != "volatility_kcli":
            dftest = adfuller(data[col].values)
            p_value = dftest[1]
            t_test = dftest[0] < dftest[4]["1%"]
            if p_value > 0.05 or not t_test:
                non_stationaries.append(col)
    
    df_stationary = data.copy()
    
 
  
    loaded_model = {}
    feature_item = {}
    with open('../TrainedModel/indicator/{}_model_2.pkl'.format(symbol), 'rb') as f:
        loaded_model = pickle.load(f)
    with open('../TrainedModel/indicator/{}_features.txt'.format(symbol), 'rb') as f:
        feature_item = pickle.load(f)
   # print(feature_item,symbol,len(feature_item))
    #print("point zero :" ,len(df_stationary.columns))

    df_stationary[non_stationaries] = df_stationary[non_stationaries].pct_change()
    df_stationary = df_stationary.iloc[1:]
    # Find NaN Rows
    na_list = df_stationary.columns[df_stationary.isna().any().tolist()]
    df_stationary.drop(columns=na_list, inplace=True)
    
    #print("point one :" ,len(df_stationary.columns))
    df_stationary = df_stationary[feature_item]
    #print("point two :" ,len(df_stationary.columns))

#    print(df_stationary)
    df_stationary = df_stationary.iloc[1:]
    
    df_stationary[np.isinf(df_stationary)] = np.nan  # Replace inf with NaN
    df_stationary = df_stationary.dropna()
    print("point three",len(df_stationary.columns),symbol)
    has_inf = "no inf data"
    if np.isinf(df_stationary).any().any():
        has_inf = "has inf data"
    df_stationary.replace(np.inf, np.nan, inplace=True)
    df_stationary.dropna(inplace=True)

        
    #print("check infifty value in",has_inf)
   # print(symbol," :",len(df_stationary.columns),len(feature_item))
    finaldata[symbol] = df_stationary 
    df_stationary = StandardScaler().fit_transform(df_stationary)
    y_pred = loaded_model.predict(df_stationary)
    y_pred = loaded_model.predict(df_stationary)

    #print("got result",symbol)
    # Specify Target

    #final training
    loaded_models[symbol] = loaded_model
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
    print(greater)
    final_result[symbol] = [current_date,train_yhat[0],1,'indicator',stock_name_only,stock_data.head(1).Close[symbol].values[0],round(greater,2)]
    result.append([current_date,train_yhat[0],1,'indicator',stock_name_only,stock_data.head(1).Close[symbol].values[0],round(greater,2)])

print(result)


# In[48]:


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


#final_target


# In[64]:


#for symbol in symbols:
  
    # Set Target (for Supervised ML later on)
 #   finaldata[symbol]["TARGET"] = -1
  #  finaldata[symbol].loc[finaldata[symbol]["Close"].shift(-1) > finaldata[symbol]["Close"], "TARGET"] = 1
   # finaldata[symbol].dropna(inplace=True)
    print()
    #retrained_model = loaded_models[symbol].fit(finaldata[symbol].iloc[:, :-1],finaldata[symbol].iloc[:, :-1])
    #with open('../TrainedModel/indicator/{}_model_2.pkl'.format(symbol), 'wb') as f:
     #   pickle.dump(retrained_model, f)

