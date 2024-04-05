from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import ccxt
import pandas as pd

from screener.database import get_currency, get_order_book, get_status, get_cubes, get_candles, get_cubes_by_symbol

from screener.exchange import get_last_prices

from screener.charts import chart_with_cubes

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
            date_get = order[9].strftime("%d/%m/%Y, %H:%M:%S")
            order_book[symbol][type][price] = {'date_start':date_start, 'date_end':date_end, 'pow':pow,
                                            'is_not_mm':is_not_mm, 'quantity':quantity, 'date_get':date_get}

        del order_book['USDCUSDT']
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
                                
                            time_live = round((order['date_end'] - order['date_start']).total_seconds() / 60)
                            if left_pips_order <= 3 and order['is_not_mm'] == True:
                                good_orders.append([symbol, type, price, order['pow'],time_live, round(left_pips_order,2), order['date_get']])
            except Exception as err:
                print(f"Error {symbol}")
        good_orders = sorted(good_orders, key=lambda x: x[5])

        return JsonResponse({'orders':good_orders})
            
    except Exception as e:
        print(e)

def index_cubes(request):
    return render(request, 'screener/index_cube.html')


def current_cube(request, symbol):
    candles = get_candles(symbol)
    df_candles = pd.DataFrame(candles, columns=['id','symbol','Open','High','Low','Close','Volume','Date'])
    cubes = get_cubes_by_symbol(symbol)
    df_cubes = pd.DataFrame(cubes, columns=['id','symbol','name_cube','Price','Date'])
    chart = chart_with_cubes(df_candles, df_cubes)

    return render(request, 'screener/current_cubes.html', {'name':symbol,'chart':chart}) 

def get_data_cubes(request):
    
    cubes = get_cubes()

    result = dict()
    for cube in cubes:
        symbol = cube[1]
        name_cube = cube[2]
        price = cube[3]
        date = cube[4]
        if symbol in result:
            if date > result[symbol]['date']:
                result[symbol]['price'] = price
                result[symbol]['date'] = date
        else:
            result[symbol] = {'name_cube':name_cube,
                              'price': price,
                              'date': date}

    res_cube = []
    now = datetime.now()
    
    for symbol, value in result.items():
        diff = round((now - value['date']).total_seconds() / 60,2)
        date = value['date'].strftime("%d/%m/%Y %H:%M:%S")
        res_cube.append([symbol, value['name_cube'], value['price'], date, diff])
    
    res_cube = sorted(res_cube, key=lambda x: x[4])

    return JsonResponse({'cubes':res_cube})


def index_status(request):
    return render(request, 'screener/status_check.html')

def get_data_status(request):
    
    status_db = get_status()

    status_list = []

    for status in status_db:
        my_list = list(status)
        my_list[3] = my_list[3].strftime("%d/%m/%Y, %H:%M:%S")
        status_list.append(my_list)
    
    return JsonResponse({'status_list':status_list})