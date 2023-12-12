import requests

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
                    if min_step_spot != 0:
                        currency_list[name + 'USDT'] = {'min_step':min_step, 'min_step_spot':min_step_spot, 'minQty': minQty,
                                                        'Name': name + 'USDT'}
                        countDone += 1
                    if countDone == upper_limit:
                        break
        except Exception as e:
            print(e)

    return currency_list

def get_last_prices():
    url = "https://api.binance.com/api/v3/ticker/bookTicker"
    data = requests.get(url).json()
    result = dict()
    for value in data:
        result[value['symbol']] = {'best_bid':float(value['bidPrice']),'best_ask':float(value['askPrice'])}
    
    return result