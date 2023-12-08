from shared_memory_dict import SharedMemoryDict
from calculations.exchange import get_currencies
import unicorn_binance_local_depth_cache
import time
from datetime import datetime
import numpy as np
import statistics
from threading import Thread
import requests

from calculations.database import insert_order_book, delete_order_book, get_order_book

from calculations.other_func import Extract, split

def get_klines(part, result,exchange):
    url = ''
    if exchange == 'S':
        url = "https://api.binance.com/api/v3/klines"
    else:
        url = "https://fapi.binance.com/fapi/v1/klines"
    for symbol in part:
        candles = requests.get(url, params={'symbol':symbol, 'interval':'5m', 'limit':20}).json()[:-1]
        res_candles = list()
        for candle in candles:
            date = datetime.fromtimestamp(int(str(candle[0])[0:10]))
            res_candles.append([float(candle[1]),float(candle[2]),float(candle[3]),float(candle[4]),float(candle[5]),date])
        result[symbol] = res_candles

def get_kline(part, result,exchange):
    url = ''
    if exchange == 'S':
        url = "https://api.binance.com/api/v3/klines"
    else:
        url = "https://fapi.binance.com/fapi/v1/klines"
    for symbol in part:
        candle = requests.get(url, params={'symbol':symbol, 'interval':'5m', 'limit':2}).json()[-2]
        res_candles = []
        date = datetime.fromtimestamp(int(str(candle[0])[0:10]))
        res_candles.append([float(candle[1]),float(candle[2]),float(candle[3]),float(candle[4]),float(candle[5]),date])
        result[symbol] = res_candles

def get_start_candles(currency_dict : dict, exchange):

    currency_list_part = split(list(currency_dict.keys()),5)

    threads = []
    result = dict()
    for part in currency_list_part:
        th = Thread(target=get_klines, args=(part, result,exchange))
        threads.append(th)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return result

def get_last_candles(currency_dict : dict,exchange):
    currency_list_part = split(list(currency_dict.keys()),5)

    threads = []
    result = dict()
    for part in currency_list_part:
        th = Thread(target=get_kline, args=(part, result,exchange))
        threads.append(th)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return result


def stream_ob(exchange):

    order_book_memory = SharedMemoryDict(name='order_book_' + exchange, size=100000000)
    aver_vol_memory = SharedMemoryDict(name='aver_volume_' + exchange, size=10000)

    list_curr = get_currencies(100)

    ubldc_s = 0

    if exchange == 'S':
        ubldc_s = unicorn_binance_local_depth_cache.BinanceLocalDepthCacheManager(exchange="binance.com")
    else:
        ubldc_s = unicorn_binance_local_depth_cache.BinanceLocalDepthCacheManager(exchange="binance.com-futures")

    order_book = dict()

    
    for symbol in list_curr:
        ubldc_s.create_depth_cache(symbol)
        order_book[symbol] = {'bids':dict(),'asks':dict()}

    order_book_db = get_order_book()

    for order in order_book_db:
        symbol = order[2]
        type = order[3]
        price = order[4]
        pow = order[5]
        quantity = order[6]
        is_not_mm = order[7]
        date_start = order[8]
        date_end = order[9]
        order_book[symbol][type][price] = {'date_start':date_start, 'date_end':date_end, 'pow':pow,
                                           'is_not_mm':is_not_mm, 'quantity':quantity}
    

    print('Get Start Candles')
    t1 = time.time()
    candles_dict = get_start_candles(list_curr, exchange)

    candles_5 = dict()
    aver_vol = dict()
    for symbol, candles in candles_dict.items():
        candles_5[symbol] = Extract(candles[-10:])
        aver_vol[symbol] = statistics.mean(candles_5[symbol])
    
    aver_vol_memory['vol'] = aver_vol

    last_minute = datetime.now().minute
    while True:
        try:
            
            new_minute = datetime.now().minute
            if last_minute != new_minute and new_minute % 5 == 0:
                print('Get last candles')
                last_candles = get_last_candles(list_curr, exchange)

                for symbol, candles in last_candles.items():
                    del candles_5[symbol][0]
                    candles_5[symbol].append(candles[0][4])
                    aver_vol[symbol] = statistics.mean(candles_5[symbol])

                aver_vol_memory['vol'] = aver_vol
                last_minute = new_minute

            t1 = time.time()
            now = datetime.now()
            for symbol in list_curr:
                bids = np.array(ubldc_s.get_bids(market=symbol))
                asks = np.array(ubldc_s.get_asks(market=symbol))
                bids = bids[bids[:,1] != 0]
                asks = asks[asks[:,1] != 0]

                max_other_order_bid = np.max(bids[:10], axis = 0)[1]
                max_orders_ask = asks[asks[:,1] / aver_vol_memory['vol'][symbol] > 2]

                dict_asks = dict()
                for order in max_orders_ask:
                    is_not_mm = False
                    if order[1] > max_other_order_bid * 2:
                        is_not_mm = True
                    if order[0] in order_book[symbol]['asks']:
                        dict_asks[order[0]] = {'date_start':order_book[symbol]['asks'][order[0]]['date_start'],
                                          'date_end':now, 'pow':np.round(order[1] / aver_vol_memory['vol'][symbol],2),
                                          'quantity':order[1], 'is_not_mm': is_not_mm}
                    else:
                        dict_asks[order[0]] = {'date_start':now, 'date_end':now, 'pow':np.round(order[1] / aver_vol_memory['vol'][symbol],2),
                                               'quantity':order[1], 'is_not_mm': is_not_mm}
                order_book[symbol]['asks'] = dict_asks

                max_other_order_ask = np.max(asks[:10], axis = 0)[1]
                max_orders_bid = bids[bids[:,1] / aver_vol_memory['vol'][symbol] > 2]

                dict_bids = dict()
                for order in max_orders_bid:
                    is_not_mm = False
                    if order[1] > max_other_order_ask * 2:
                        is_not_mm = True
                    if order[0] in order_book[symbol]['bids']:
                        dict_bids[order[0]] = {'date_start':order_book[symbol]['bids'][order[0]]['date_start'],
                                          'date_end':now, 'pow':np.round(order[1] / aver_vol_memory['vol'][symbol],2),
                                          'quantity':order[1], 'is_not_mm': is_not_mm}
                    else:
                        dict_bids[order[0]] = {'date_start':now, 'date_end':now, 'pow':np.round(order[1] / aver_vol_memory['vol'][symbol],2),
                                               'quantity':order[1], 'is_not_mm': is_not_mm}
                order_book[symbol]['bids'] = dict_bids
            
            print(f"Time spend Order Book {exchange} {time.time() - t1}")
            delete_order_book()
            insert_order_book(order_book)
            order_book_memory['order_book'] = order_book
            time.sleep(10)
        except Exception as e:
            print(e)
            time.sleep(1)
    

if __name__ == '__main__':
    stream_ob('S')