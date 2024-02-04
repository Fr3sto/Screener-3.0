import requests
from pybit.unified_trading import HTTP
import ccxt
import pandas as pd
import datetime as dt

def get_candles_by_date(exchange, type_exchange, symbol, from_date, to_date, limit=1000):
    try:
        df = pd.DataFrame()
        startTime = str(int(from_date.timestamp() * 1000))
        endTime   = str(int(to_date.timestamp() * 1000))
        startDate = startTime
        candles = []
        tf = 5 if exchange == 'Bybit' else '5m'
        par = 'start' if exchange == 'Bybit' else 'startTime'
        while startDate<endTime:
            if startDate is not None:
                candles = exchange_machines[exchange][type_exchange].fetch_ohlcv(symbol, tf, None, limit, {par: startDate})
            else:
                candles = exchange_machines[exchange][type_exchange].fetch_ohlcv(symbol, tf, None, limit)
            
            if len(candles) == 1:
                break
            
            df2 = pd.DataFrame(candles)
            df2.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            df = pd.concat([df2, df], axis=0, ignore_index=True, keys=None)
            startDate = str(candles[-1][0])  

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


exchange_binance_spot = ccxt.binance({'options': {
    'defaultType': 'spot'}})

exchange_binance_future = ccxt.binance({'options': {
    'defaultType': 'future'}})

exchange_bybit_spot = ccxt.bybit({'options': {
    'defaultType': 'spot'}})

exchange_bybit_future = ccxt.bybit({'options': {
    'defaultType': 'linear'}})

exchange_machines = dict()
exchange_machines['Binance'] = {'Spot':exchange_binance_spot, 'Future':exchange_binance_future}
exchange_machines['Bybit'] = {'Spot':exchange_bybit_spot, 'Future':exchange_bybit_future}



def get_all_last_prices():
    res_binance_s = get_last_prices_binance_s()
    res_binance_f = get_last_prices_binance_f()

    res_bybit_s = get_last_prices_bybit_s()
    res_bybit_f = get_last_prices_bybit_f()

    result = dict()
    result['Binance'] = {'Spot':res_binance_s, 'Future': res_binance_f}
    result['Bybit'] = {'Spot':res_bybit_s,'Future':res_bybit_f}

    return result


def get_last_prices_binance_s():
    url = "https://api.binance.com/api/v3/ticker/bookTicker"
    data = requests.get(url).json()
    result = dict()
    for value in data:
        if 'USDT' in value['symbol']:
            result[value['symbol'].split('USDT')[0] + '/USDT'] = {'best_bid':float(value['bidPrice']),'best_ask':float(value['askPrice'])}
    
    return result

def get_last_prices_binance_f():
    url = "https://fapi.binance.com/fapi/v1/ticker/bookTicker"
    data = requests.get(url).json()
    result = dict()
    for value in data:
        if 'USDT' in value['symbol']:
            result[value['symbol']] = {'best_bid':float(value['bidPrice']),'best_ask':float(value['askPrice'])}
    
    return result

def get_last_prices_bybit_f():
    session = HTTP()
    data = session.get_tickers(category="linear")    
    result = dict()
    for value in data['result']['list']:
        if 'USDT' in value['symbol']:
            result[value['symbol']] = {'best_bid':float(value['bid1Price']),'best_ask':float(value['ask1Price']), 'last_price':float(value['lastPrice'])}
    
    return result

def get_last_prices_bybit_s():
    session = HTTP()
    data = session.get_tickers(category="spot")    
    result = dict()
    for value in data['result']['list']:
        if 'USDT' in value['symbol']:
            result[value['symbol'].split('USDT')[0] + '/USDT'] = {'best_bid':float(value['bid1Price']),'best_ask':float(value['ask1Price']), 'last_price':float(value['lastPrice'])}
    
    return result