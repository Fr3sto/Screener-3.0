import requests
from pybit.unified_trading import HTTP
import ccxt

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