
from smartapi import SmartConnect
from smartapi.smartWebSocketV2 import SmartWebSocketV2
import os
import urllib
import json
import pandas as pd
import datetime as dt
from pyotp import TOTP
from ta import trend
from ta.volatility import AverageTrueRange


key_path = r"/Users/vipin/workspace/ai/my_own"
os.chdir(key_path)

key_secret = open("key.txt","r").read().split()

obj=SmartConnect(api_key=key_secret[0])
data = obj.generateSession(key_secret[2],key_secret[3],TOTP(key_secret[4]).now())
feed_token = obj.getfeedToken()

instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = urllib.request.urlopen(instrument_url)
instrument_list = json.loads(response.read())

def token_lookup(ticker, instrument_list, exchange="NSE"):
    for instrument in instrument_list:
        if instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[-1] == "EQ":
            return instrument["token"]
        
def symbol_lookup(token, instrument_list, exchange="NSE"):
    for instrument in instrument_list:
        if instrument["token"] == token and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[-1] == "EQ":
            return instrument["name"]


def hist_data(tickers,duration,interval,instrument_list,exchange="NSE"):
    hist_data_tickers = {} 
    for ticker in tickers:
        params = {
                 "exchange": exchange,
                 "symboltoken": token_lookup(ticker,instrument_list),
                 "interval": interval,
                 "fromdate": (dt.date.today() - dt.timedelta(duration)).strftime('%Y-%m-%d %H:%M'),
                 "todate": dt.date.today().strftime('%Y-%m-%d %H:%M')  
                 }
        hist_data = obj.getCandleData(params)
        df_data = pd.DataFrame(hist_data["data"],
                               columns = ["date","open","high","low","close","volume"])
        df_data.set_index("date",inplace=True)
        df_data.index = pd.to_datetime(df_data.index)
        df_data.index = df_data.index.tz_localize(None)
        hist_data_tickers[ticker] = df_data
    return hist_data_tickers

def merge_with_historical_data(new_data,historical_data):
    new_df = pd.DataFrame(new_data)
    new_df['date'] = pd.to_datetime(new_df['date'])
    new_df = new_df.set_index('date')
    return pd.concat([historical_data,new_df])
    

candle_data = hist_data(["HDFC"], 50, "ONE_HOUR", instrument_list)
new_data = {
    'date': ['2024-06-01 12:00:00', '2024-06-01 13:00:00'],
    'close': [40, 50],
    'high': [40, 50],
    'low': [40, 50],
    'open': [40, 50],
    'volume': [40, 50]
}
close_his = candle_data["HDFC"]
merged_df = merge_with_historical_data(new_data,close_his)


window = 5

sma = trend.sma_indicator(close = merged_df["close"], window=window)
ema = trend.ema_indicator(close = merged_df["close"], window=window)

# Calculate ATR
atr = AverageTrueRange(high=merged_df['high'], low=merged_df['low'], close=merged_df['close'], window=14)
atr_values = atr.average_true_range()

dataLen = len(sma) - 1

# Print SMA values
print(sma[dataLen],ema[dataLen],atr_values[dataLen])

sws = SmartWebSocketV2(data["data"]["jwtToken"], key_secret[0], key_secret[2], feed_token)


correlation_id = "stream_1" #any string value which will help identify the specific streaming in case of concurrent streaming
action = 1 #1 subscribe, 0 unsubscribe
mode = 2 #1 for LTP, 2 for Quote and 2 for SnapQuote
tickers = ["HDFC"]
token_list = [{"exchangeType": 1, "tokens": [token_lookup(i,instrument_list) for i in tickers]}]

def on_data(ws, message):
    print(message)
    
def on_open(ws):
    print("on open")
    sws.subscribe(correlation_id, mode, token_list)
    
def on_error(ws, error):
    print(error)
    

# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error

sws.connect()





















