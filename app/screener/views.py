from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import ccxt
import pandas as pd

from screener.database import get_currency, get_order_book

from screener.exchange import get_last_prices


def index(request):
    return render(request, 'screener/big_orders.html')

all_currency = get_currency()

def get_data_order_book(request):
    try:

        
        order_book = dict()
        
        for symbol in all_currency.keys():
            order_book[symbol] = {'asks':{}, 'bids':{}}

        order_book_db = get_order_book()

        for order in order_book_db:
            symbol = order[1]
            type = order[2]
            price = order[3]
            pow = order[4]
            quantity = order[5]
            is_not_mm = order[6]
            date_start = order[7]
            date_end = order[8]
            order_book[symbol][type][price] = {'date_start':date_start, 'date_end':date_end, 'pow':pow,
                                            'is_not_mm':is_not_mm, 'quantity':quantity}

        last_prices = get_last_prices()

        good_orders = []
        for symbol, types in order_book.items():
            try:
                best_bid = last_prices[symbol]['best_bid']
                best_ask = last_prices[symbol]['best_ask']
                for type, prices in types.items():
                    for price, order in prices.items():
                        order_count_decimal = str(round(price / all_currency[symbol]['min_step']))
                        left_pips_order = 0
                        if order_count_decimal[-1] == '0':
                            if type == 'asks':
                                left_pips_order = 100 - best_ask / price * 100
                            else:
                                left_pips_order = 100 - price / best_bid * 100
                                
                            time_live = round((order['date_end'] - order['date_start']).seconds / 60)
                            if left_pips_order <= 3 and order['is_not_mm'] == True:
                                good_orders.append([symbol, type, price, order['pow'],time_live, round(left_pips_order,2)])
            except Exception as err:
                print(f"Error {symbol}")
        good_orders = sorted(good_orders, key=lambda x: x[5])

        return JsonResponse({'orders':good_orders})
            
    except Exception as e:
        print(e)

    