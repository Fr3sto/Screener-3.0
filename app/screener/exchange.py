import requests


from pybit.unified_trading import HTTP

def get_last_prices_f():
    session = HTTP()
    data = session.get_tickers(category="linear")    
    result = dict()
    for value in data['result']['list']:
        result[value['symbol']] = {'best_bid':float(value['bid1Price']),'best_ask':float(value['ask1Price']), 'last_price':float(value['lastPrice'])}
    
    return result