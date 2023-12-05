import requests
from datetime import datetime

def get_currencies(upper_limit : int):
    
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    url_spot = 'https://api.binance.com/api/v3/exchangeInfo'

    data = requests.get(url).json()
    data_s = requests.get(url_spot).json()

    bad_currency = ['USDC','TUSD','BUSD','USDP', 'BTCDOWN', 'BTCUP','1000SHIB', 'DEFI', 'BTCDOM']
    currency_list = dict()
    countDone = 0
    for symbol in data['symbols']:
        try:
            name = symbol['baseAsset']
            pair = symbol['quoteAsset']
            # symbol = key.split('/')[0]
            # future = key.split(':')
            if name in bad_currency:
                continue

            if pair == 'USDT':
                if symbol['status'] == 'TRADING' and symbol['contractType'] == 'PERPETUAL':
                    min_step = float(symbol['filters'][0]['tickSize'])
                    minQty = float(symbol['filters'][1]['minQty'])
                    min_step_spot = 0
                    for symbol_spot in data_s['symbols']:
                        if symbol['symbol'] == symbol_spot['symbol']:
                            min_step_spot = float(symbol_spot['filters'][0]['tickSize'])
                            break
                    if name + 'USDT' == 'IOTXUSDT':
                        s = 5
                    if min_step_spot != 0:
                        currency_list[name + 'USDT'] = {'min_step':min_step, 'min_step_spot':min_step_spot, 'minQty': minQty,
                                                        'Name': name + 'USDT', 'pricePrecision':symbol['pricePrecision']}
                        countDone += 1
                    if countDone == upper_limit:
                        break
        except Exception as e:
            print(e)

    return currency_list

def get_klines(result, part, interval, TF, take_count):
    #url = "https://fapi.binance.com/fapi/v1/klines"
    url = "https://api.binance.com/api/v3/klines"
    for symbol in part:
        candles = requests.get(url, params={'symbol':symbol, 'interval':interval, 'limit':take_count}).json()[:-1]
        res_candles = list()
        for candle in candles:
            date = datetime.fromtimestamp(int(str(candle[0])[0:10]))
            res_candles.append([float(candle[1]),float(candle[2]),float(candle[3]),float(candle[4]),float(candle[5]),date])
        result[str(symbol) + '-' + str(TF)] = res_candles

def get_kline(result, part, interval, TF):
    url = "https://api.binance.com/api/v3/klines"
    for symbol in part:
        candle = requests.get(url, params={'symbol':symbol, 'interval':interval, 'limit':2}).json()[-2]
        res_candles = []
        date = datetime.fromtimestamp(int(str(candle[0])[0:10]))
        res_candles.append([float(candle[1]),float(candle[2]),float(candle[3]),float(candle[4]),float(candle[5]),date])
        result[str(symbol) + '-' + str(TF)] = res_candles

def get_last_prices_f_all():
    url = "https://fapi.binance.com/fapi/v1/ticker/bookTicker"
    data = requests.get(url).json()
    result = dict()
    for value in data:
        result[value['symbol']] = {'best_bid':float(value['bidPrice']),'best_ask':float(value['askPrice'])}
    
    return result

def get_last_prices_f(symbol_list):
    url = "https://fapi.binance.com/fapi/v1/ticker/bookTicker"
    data = requests.get(url).json()
    result = dict()
    for value in data:
        if value['symbol'] in symbol_list:
            result[value['symbol']] = {'best_bid':float(value['bidPrice']),'best_ask':float(value['askPrice'])}
    
    return result

def get_last_prices_s(symbol_list):
    url = "https://api.binance.com/api/v3/ticker/bookTicker"
    data = requests.get(url).json()
    result = dict()
    for value in data:
        if value['symbol'] in symbol_list:
            result[value['symbol']] = {'best_bid':float(value['bidPrice']),'best_ask':float(value['askPrice'])}
    
    return result