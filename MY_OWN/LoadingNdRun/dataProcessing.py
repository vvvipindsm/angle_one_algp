import numpy as np
import pandas as pd
from stratmanagerDaily import StrategyManager
import sklearn.mixture as mix
from ta.momentum import RSIIndicator
import matplotlib.pyplot as plt
import yfinance

class DataProcessing():

    # Initialize the class
    def __init__(self,symbol,data):
        self.df = self.execu(symbol,data)
       
     # run data
    def execu(self,symbol,data):
       # Extract Data
        start_date = "2005-01-1"
        end_date = "2022-06-1"

        symbol = "TATAMOTORS.NS"
        strat_mgr = StrategyManager(symbol, start_date, end_date,data)
        df = strat_mgr.df.copy()
        df_fe = df.copy()
        # Add RSI
        rsi = RSIIndicator(close=df_fe["Close"], window=14).rsi()
        df_fe["RSI"] = rsi
        df_fe["RSI_Ret"] = df_fe["RSI"] / df_fe["RSI"].shift(1)
        
         # Add Moving Average
        df_fe["MA_12"] = df_fe["Close"].rolling(window=12).mean()
        df_fe["MA_21"] = df_fe["Close"].rolling(window=21).mean()
        # Day of Week
        #df_fe["DOW"] = df_fe.index.dayofweek
        # Rolling Cumulative Returns
        df_fe["Roll_Rets"] = df_fe["Returns"].rolling(window=30).sum()
        # Rolling Cumulative Range
        df_fe["Avg_Range"] = df_fe["Range"].rolling(window=30).mean()
        
        # Add Time Intervals
        t_steps = [1, 2]
        t_features = ["Returns", "Range", "RSI_Ret"]
        for ts in t_steps:
            for tf in t_features:
                df_fe[f"{tf}_T{ts}"] = df_fe[tf].shift(ts)
                
        df_fs = df_fe.copy()
        df_fs[["Open", "High", "Low", "Volume"]] = df_fs[["Open", "High", "Low", "Volume"]].pct_change()
        #df_fs
        # Check for NaN
        df_fs.dropna(inplace=True)
        #print(df_fs.isnull().values.any())
        return df_fs
    
     
