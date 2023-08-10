#!/usr/bin/env python
# coding: utf-8

# #Libraries and Data

# In[28]:


#import libraries
import numpy as np
import pandas as pd
import itertools
import yfinance
from datetime import datetime


# In[29]:


def load_and_setup_data(sybmol,input_data):
    df = pd.read_csv("../stock_historical_data/{}.csv".format(sybmol))
    df.set_index("Date", inplace=True)
    new_data = pd.DataFrame(input_data)
    new_data.set_index("Date", inplace=True)
    concatenated_df = pd.concat([df,new_data])
    concatenated_df.to_csv("../stock_historical_data/{}.csv".format(sybmol))

   # print(concatenated_df)
    print(concatenated_df)
    return concatenated_df

def fetch_stock_data(tickers):
    data = yfinance.download(tickers,period='1d')
    #print(data)
    return data
    


# In[30]:


#symbols = ["OLECTRA.NS","LT.NS","CONCOR.NS","ELGIEQUIP.NS","IOC.NS","BEL.NS","TATAELXSI.NS","^NSEI"]
symbols = ["OLECTRA.NS","CONCOR.NS","ELGIEQUIP.NS","IOC.NS","BEL.NS","TATAELXSI.NS","^NSEI","RELI","HDFCBANK.NS","TATAMOTORS.NS","SBIN.NS","TCS.NS","TITAN.NS","SUNPHARMA.BO","TECHM.NS", "ASIANPAINT.NS","TATACONSUM.NS","INR=X","^DJI","^FTSE","BTC-USD","^VIX","RTY=F","USDCNY=X","CL=F","GC=F","^NSEBANK" , "^CNXFMCG","NIFTY_FIN_SERVICE.NS","^CNXIT","NIFTY_PVT_BANK.NS","^CNXMETAL"]
#symbols = ["OLECTRA.NS","HDFCBANK.NS"]
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


# In[31]:


stock_data.tail(1)


# In[32]:


finaldata = {}
current_date = datetime.now().strftime("%d-%m-%Y")

for symbol in symbols:
    stock_name = symbol
    if symbol == "^NSEI":
        stock_name = "NSEI"
    #print(symbol)
    input_data = {
                    # "Open" : stock_data.head(1).Open[ticker].values[0],
                    "Open" : [stock_data.tail(1).Open[symbol].values[0]],
                    "Close" : [stock_data.tail(1).Close[symbol].values[0]],
                    "High" : [stock_data.tail(1).High[symbol].values[0]],
                    "Low" : [stock_data.tail(1).Low[symbol].values[0]], 
                    "Volume" : [stock_data.tail(1).Volume[symbol].values[0]],
                    "Date":[np.datetime_as_string(stock_data.index, unit='D')[0]]
    }   
    print(input_data)
    data = load_and_setup_data(symbol,input_data)
    

