import requests
from pybit.unified_trading import HTTP
import ccxt
import pandas as pd
import datetime as dt
from datetime import datetime


def get_candles_by_date(symbol, from_date, to_date, limit=1000):
    try:
        df = pd.DataFrame()
        startTime = str(int(from_date.timestamp() * 1000))
        endTime   = str(int(to_date.timestamp() * 1000))
        candles = []
        tf = 5
        par = 'start'
        while startTime<endTime:
            if startTime is not None:
                candles = exchange_bybit_future.fetch_ohlcv(symbol, tf, None, limit, {par: startTime})
            else:
                candles = exchange_bybit_future.fetch_ohlcv(symbol, tf, None, limit)
            
            if len(candles) == 1:
                break
            
            df2 = pd.DataFrame(candles)
            df2.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            df = pd.concat([df2, df], axis=0, ignore_index=True, keys=None)
            startTime = str(candles[-1][0])  

        df.reset_index(drop=True, inplace=True)    
        df['Date'] = [dt.datetime.fromtimestamp(int(str(x)[0:10])) for x in df['Date']]
        df['Open'] = [float(x) for x in df['Open']]
        df['High'] = [float(x) for x in df['High']]
        df['Low'] = [float(x) for x in df['Low']]
        df['Close'] = [float(x) for x in df['Close']]

        usecols=['Open', 'High', 'Low', 'Close', 'Volume', 'Date']
        df = df[usecols]
        df.sort_values(by='Date', inplace = True) 

        return df
    except Exception as e:
        print(e)


exchange_bybit_future = ccxt.bybit({'options': {
    'defaultType': 'linear'}})

from pybit.unified_trading import HTTP

def get_all_min_step():

    session = HTTP(testnet=False)
    result_info = session.get_instruments_info(
        category="linear",
    )

    result = {}

    for el in result_info['result']['list']:
        symbol = el['symbol']
        min_step = el['priceFilter']['tickSize']

        result[symbol] = {'min_step':min_step}

    return result

def get_last_prices():
    session = HTTP()
    data = session.get_tickers(category="linear")    
    result = dict()
    for value in data['result']['list']:
        if 'USDT' in value['symbol']:
            result[value['symbol']] = {'best_bid':float(value['bid1Price']),'best_ask':float(value['ask1Price']), 'last_price':float(value['lastPrice'])}
    
    return result