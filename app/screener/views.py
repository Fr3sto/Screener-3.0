from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime


from screener.services import collect_all_data_for_screener
from screener.database import  get_all_positions,get_all_currency, get_all_order_book, get_close_levels, get_all_deals, get_all_status_check
from screener.charts import get_order_book_chart

from screener.exchange import get_last_prices, get_currencies

currency_list = get_all_currency()

def index(request):

    try:
        print('Good')
        data = collect_all_data_for_screener(curr_list)
        list_tf = [5,15,30,60]

        return render(request, 'screener/index.html', {'data':data, 'list_tf':list_tf})
    except Exception as e:
        print(e)

def big_orders(request):
    return render(request, 'screener/big_orders.html')

curr_list = get_currencies(100)

def get_data(request):
    good_orders = []
    try:
        order_book_list = get_all_order_book()
        order_book = dict()

        for currency in currency_list:
            order_book[currency[1]] = {'bids':dict(),'asks':dict()}


        for order in order_book_list:
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
        for symbol, types in order_book.items():
            best_bid = last_prices[symbol]['best_bid']
            best_ask = last_prices[symbol]['best_ask']

            for type, orders in types.items():
                for price, order in orders.items():
                    order_count_decimal = str(round(price / curr_list[symbol]['min_step_spot']))
                    
                    if order_count_decimal[-1] == '0':
                        if type == 'asks':
                            left_pips_order = 100 - best_ask / price * 100
                        else:
                            left_pips_order = 100 - price / best_bid * 100
                            
                        time_live = round((order['date_end'] - order['date_start']).seconds / 60)
                        if left_pips_order <= 6 and time_live > 30 and order['is_not_mm'] == True:
                            good_orders.append([symbol, type, price, order['pow'],time_live, round(left_pips_order,2)])
        good_orders = sorted(good_orders, key=lambda x: x[5])


        close_levels = get_close_levels()

        close_levels_result = []

        for index, value in enumerate(close_levels):
            my_list = list(close_levels[index])
            my_list[8] = round(my_list[8],2)
            my_list[9] = str((datetime.now() - my_list[9])).split('.')[0]
            close_levels_result.append(my_list)

        close_levels_result = sorted(close_levels_result, key=lambda x: x[4])

    except Exception as e:
        print(e)
    
    
    return JsonResponse({'close_levels':close_levels_result, 'orders':good_orders})

def status_check(request):
    return render(request, 'screener/status_check.html')

def get_data_status(request):

    status_check_list = get_all_status_check()

    result_status = []

    for status in status_check_list:
        my_list = list(status)
        my_list[3] =  my_list[3].strftime("%d/%m/%Y, %H:%M:%S")
        result_status.append(my_list)

    return JsonResponse({'status_list':result_status})

def positions(request):
    return render(request, 'screener/positions.html')

def get_data_position(request):
    
    positions = get_all_positions()
    result_positions = []

    for pos in positions:
        my_list = list(pos)
        my_list[5] =  my_list[5].strftime("%d/%m/%Y, %H:%M:%S")
        result_positions.append(my_list)

    deals = get_all_deals()
    result_deals = []

    for deal in deals:
        my_list = list(deal)
        my_list[5] =  my_list[5].strftime("%d/%m/%Y, %H:%M:%S")
        my_list[7] =  my_list[7].strftime("%d/%m/%Y, %H:%M:%S")
        result_deals.append(my_list)
    return JsonResponse({'positions':result_positions, 'deals':result_deals})

from screener.services import get_currency_chart_with_impulse

def currency_chart(request, symbol, tf):
    print(symbol, tf)
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



