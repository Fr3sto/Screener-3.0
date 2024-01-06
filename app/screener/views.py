from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime


from screener.services import collect_all_data_for_screener
from screener.database import  (get_all_positions,get_all_currency, get_all_order_book_s,
                                get_all_order_book_f, get_close_levels, get_all_deals, 
                                get_all_status_check, get_deal_by_id, get_all_levels)
from screener.charts import get_order_book_chart, get_chart_deal, get_chart_deal_zoom, get_chart_level, get_chart_close_levels, get_chart_close_level

from screener.exchange import get_last_prices_s, get_last_prices_f, get_currencies

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

def chart_close_levels(request):
    charts = get_chart_close_levels()
    return render(request, 'screener/close_levels.html', {'charts':charts})

def chart_close_level(request, symbol):
    chart = get_chart_close_level(symbol)
    return render(request, 'screener/close_level.html', {'chart':chart, 'name':symbol})


def get_data(request):
    good_orders_s = []
    good_orders_f = []
    close_levels_result = []
    try:
        order_book_list = get_all_order_book_s()
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


        
        last_prices = get_last_prices_s()
        for symbol, types in order_book.items():
            best_bid = last_prices[symbol]['best_bid']
            best_ask = last_prices[symbol]['best_ask']

            if symbol == 'TRXUSDT':
                pass
            for type, orders in types.items():
                for price, order in orders.items():
                    order_count_decimal = str(round(price / curr_list[symbol]['min_step_spot']))
                    
                    if order_count_decimal[-1] == '0':
                        if type == 'asks':
                            left_pips_order = 100 - best_ask / price * 100
                        else:
                            left_pips_order = 100 - price / best_bid * 100

                        time_live = round((order['date_end'] - order['date_start']).seconds / 60)
                        if left_pips_order <= 3 and order['is_not_mm'] == True:
                            good_orders_s.append([symbol, type, price, order['pow'],time_live, round(left_pips_order,2)])
        good_orders_s = sorted(good_orders_s, key=lambda x: x[5])


        order_book_list = get_all_order_book_f()
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


        
        last_prices = get_last_prices_f()
        for symbol, types in order_book.items():
            best_bid = last_prices[symbol]['best_bid']
            best_ask = last_prices[symbol]['best_ask']

            for type, orders in types.items():
                for price, order in orders.items():
                    order_count_decimal = str(round(price / curr_list[symbol]['min_step']))
                    
                    if order_count_decimal[-1] == '0':
                        if type == 'asks':
                            left_pips_order = 100 - best_ask / price * 100
                        else:
                            left_pips_order = 100 - price / best_bid * 100
                            
                        time_live = round((order['date_end'] - order['date_start']).seconds / 60)
                        if left_pips_order <= 3 and order['is_not_mm'] == True:
                            good_orders_f.append([symbol, type, price, order['pow'],time_live, round(left_pips_order,2)])
        good_orders_f = sorted(good_orders_f, key=lambda x: x[5])


        levels = get_all_levels()

        levels_dict = dict()

        for level in levels:
            symbol = level[1]
            price = level[3]
            type = level[4]
            date_start = level[5]

            if not symbol in levels_dict:
                levels_dict[symbol] = {1 : [], 2 : []}

            levels_dict[symbol][type].append((price, date_start))
        
        for symbol, type in levels_dict.items():
            levels_1 = sorted(type[1], key=lambda x: x[0], reverse=True)

            if len(levels_1) > 2:
                for i in range(2, len(levels_1)):
                    left_1 = 100 - levels_1[i][0] / levels_1[i - 1][0] * 100
                    left_2 = 100 - levels_1[i][0] / levels_1[i - 2][0] * 100
                    if left_1 < 0.3 and left_2 < 0.3:
                        #print(f"{symbol} Close levels Up {levels_1[i][0]} {levels_1[i - 1][0]} {levels_1[i - 2][0]}")
                        best_ask = last_prices[symbol]['best_ask']
                        left_pips = round(100 - best_ask / levels_1[i][0] * 100, 2)
                        close_levels_result.append((symbol, 1, levels_1[i][0], levels_1[i -1][0], levels_1[i - 2][0], left_pips))
                    

            
            levels_2 = sorted(type[2], key=lambda x: x[0], reverse=True)

            if len(levels_2) > 2:
                for i in range(2, len(levels_2)):
                    left_1 = 100 - levels_2[i][0] / levels_2[i - 1][0] * 100
                    left_2 = 100 - levels_2[i][0] / levels_2[i - 2][0] * 100
                    if left_1 < 0.3 and left_2 < 0.3:
                        #print(f"{symbol} Close levels Down {levels_2[i][0]} {levels_2[i - 1][0]} {levels_2[i - 2][0]}")
                        best_bid = last_prices[symbol]['best_bid']
                        left_pips = round(100 - levels_2[i - 2][0] / best_bid * 100, 2)
                        close_levels_result.append((symbol, 2, levels_2[i][0], levels_2[i -1][0], levels_2[i - 2][0], left_pips))
                    

        close_levels_result = sorted(close_levels_result, key=lambda x: x[5])

    except Exception as e:
        print(e)
    
    
    return JsonResponse({'close_levels':close_levels_result, 'orders_s':good_orders_s, 'orders_f':good_orders_f})

def current_level(request, id):
    chart = get_chart_level(id)
    return render(request, 'screener/current_level.html', {'chart':chart})

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
    result_positions = []
    result_deals = []
    try:
        positions = get_all_positions()
        

        for pos in positions:
            my_list = list(pos)
            my_list[5] =  my_list[5].strftime("%d/%m/%Y, %H:%M:%S")
            result_positions.append(my_list)

        deals = get_all_deals()
        

        for deal in deals:
            my_list = list(deal)
            my_list[5] =  my_list[5].strftime("%d/%m/%Y, %H:%M:%S")
            my_list[7] =  my_list[7].strftime("%d/%m/%Y, %H:%M:%S")
            result_deals.append(my_list)
    except Exception as e:
        print(e)
    return JsonResponse({'positions':result_positions, 'deals':result_deals})

def current_deal(request, id):
    print(id)
    deals = get_deal_by_id(int(id))
    symbol = deals[0][1]
    chart = get_chart_deal(deals[0])
    chart_2 = get_chart_deal_zoom(deals[0])
    return render(request, 'screener/current_deal.html', {'name':symbol,'chart':chart, 'chart_2':chart_2})



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



