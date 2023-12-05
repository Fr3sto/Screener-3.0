from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from shared_memory_dict import SharedMemoryDict

from screener.services import collect_data_for_levels, collect_all_data_for_screener
from screener.database import get_all_close_levels, get_all_positions
from screener.charts import get_order_book_chart, get_levels_chart

from screener.exchange import get_last_prices, get_currencies


def index(request):

    data = collect_all_data_for_screener()
    list_tf = [5,15,30,60]

    return render(request, 'screener/index.html', {'data':data, 'list_tf':list_tf})

curr_list = get_currencies(100)

def get_data(request):
    close_levels = get_all_close_levels()

    result_list = []
    for index, value in enumerate(close_levels):
        my_list = list(close_levels[index])
        symbol = my_list[1]
        price_level = my_list[2]
        type_level = my_list[3]
        left_pips = my_list[4]
        price_order_s = my_list[5]
        pow_s = my_list[6]
        time_live_s = my_list[7]

        left_Pips_order_s = 0

        if price_order_s > 1000000 or price_order_s == 0:
            price_order_s = 0
            pow_s = 0
            time_live_s = 0
        else:
            time_live_s = str((datetime.now() - time_live_s)).split('.')[0]
            left_Pips_order_s = 0
            if type_level == 1:
                currPrice = price_level - price_level * left_pips / 100
                left_Pips_order_s = (price_order_s - currPrice) / (currPrice / 100)
            else:
                currPrice = price_level + price_level * left_pips / 100
                left_Pips_order_s = (currPrice - price_order_s) / (currPrice / 100)
            left_Pips_order_s = round(left_Pips_order_s,2)
            result_list.append([symbol, price_level,type_level,left_pips,
                                price_order_s,pow_s,time_live_s,left_Pips_order_s])
    
    
    result_list = sorted(result_list, key=lambda x: x[7])

    positions = get_all_positions()

    res_positions = []
    for pos in positions:
        my_list = list(pos)
        my_list[4] = my_list[4].strftime("%H:%M:%S %d/%m/%Y")
        res_positions.append(my_list)

    positions = res_positions

    order_book_memory = SharedMemoryDict(name='order_book', size=1000000)
    aver_vol_memory = SharedMemoryDict(name='aver_volume', size=10000)
    good_orders = []
    last_prices = get_last_prices()
    order_book_copy = order_book_memory['order_book'].copy()
    for symbol, order_book in order_book_copy.items():
        best_bid = last_prices[symbol]['best_bid']
        best_ask = last_prices[symbol]['best_ask']

        for type, orders in order_book.items():
            for price, order in orders.items():
                order_count_decimal = str(int(price / curr_list[symbol]['min_step_spot']))
                
                if order_count_decimal[-1] == '0':
                    if type == 'asks':
                        left_pips_order = 100 - best_ask / price * 100
                    else:
                        left_pips_order = 100 - price / best_bid * 100
                        
                    time_live = round((order['date_end'] - order['date_start']).seconds / 60)
                    if left_pips_order <= 6 and time_live > 30 and order['is_not_mm'] == True:
                        good_orders.append([symbol, type, price, order['pow'],time_live, round(left_pips_order,2)])

    good_orders = sorted(good_orders, key=lambda x: x[5])
    return JsonResponse({'close_levels':result_list, 'positions':positions, 'orders':good_orders})

from screener.services import get_currency_chart_with_impulse

def currency_chart(request, symbol, tf):
    chart = get_currency_chart_with_impulse(symbol,tf)
    return render(request, 'screener/currency_chart.html', {'chart':chart})


import os
def order_book_chart(request, symbol):
    charts = []

    files = os.listdir("signal_order/")
    done = 0
    for file in files:
        try:
            name = file.split('.')[0]
            chart = get_order_book_chart(name)
            charts.append(chart)
            done += 1
            print(f"{done}/{len(files)}")
        except Exception as e:
            print(e)
    #charts.append(get_order_book_chart(symbol))
    
    return render(request, 'screener/order_book_chart.html', {'charts' : charts})

def levels_chart(request, symbol):
    chart = get_levels_chart(symbol)
    return render(request, 'screener/levels_chart.html', {'chart' : chart})



