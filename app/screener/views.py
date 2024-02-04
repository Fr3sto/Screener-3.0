from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import ccxt


from screener.database import  (get_all_positions,get_all_currency,
                                 get_close_levels, get_all_deals, 
                                 get_deal_by_id, get_all_levels, get_all_status_check, get_all_order_books, get_all_symbols_for_order_book,
                                 get_position_by_id)
from screener.charts import (  get_chart_deal_rebound_level, get_chart_deal_rebound_level_zoom, get_chart_equity,
                                get_chart_current_position)

from screener.exchange import get_all_last_prices

from screener.services import get_close_three_levels, get_close_two_levels


def big_orders(request):
    return render(request, 'screener/big_orders.html')

all_currency = get_all_symbols_for_order_book()

def get_data_order_book(request):
    all_good_orders = dict()

    good_levels = []
    try:

        
        all_order_book = dict()

        for exchange, types in all_currency.items():
            if not exchange in all_order_book:
                all_order_book[exchange] = {'Spot':dict(), 'Future': dict()}
                all_good_orders[exchange] = {'Spot':[], 'Future': []}

            for type, symbols in types.items():
                for symbol in symbols:
                    all_order_book[exchange][type][symbol] = {'asks':{}, 'bids':{}}

        order_book_db = get_all_order_books()

        for order in order_book_db:
            exchange = order[1]
            type_exchange = order[2]
            symbol = order[3]
            type = order[4]
            price = order[5]
            pow = order[6]
            quantity = order[7]
            is_not_mm = order[8]
            date_start = order[9]
            date_end = order[10]
            all_order_book[exchange][type_exchange][symbol][type][price] = {'date_start':date_start, 'date_end':date_end, 'pow':pow,
                                            'is_not_mm':is_not_mm, 'quantity':quantity}

        last_prices = get_all_last_prices()

        for exchange, type_exchanges in all_order_book.items():
            for type_exchange, symbols in type_exchanges.items():
                good_orders = []
                for symbol, types in symbols.items():
                    best_bid = last_prices[exchange][type_exchange][symbol]['best_bid']
                    best_ask = last_prices[exchange][type_exchange][symbol]['best_ask']
                    for type, prices in types.items():
                        for price, order in prices.items():
                            order_count_decimal = str(round(price / all_currency[exchange][type_exchange][symbol]['min_step']))
                            left_pips_order = 0
                            if order_count_decimal[-1] == '0':
                                if type == 'asks':
                                    left_pips_order = 100 - best_ask / price * 100
                                else:
                                    left_pips_order = 100 - price / best_bid * 100
                                    
                                time_live = round((order['date_end'] - order['date_start']).seconds / 60)
                                if left_pips_order <= 3 and order['is_not_mm'] == True:
                                    good_orders.append([symbol, type, price, order['pow'],time_live, round(left_pips_order,2)])
                good_orders = sorted(good_orders, key=lambda x: x[5])
                all_good_orders[exchange][type_exchange] = good_orders

            

    except Exception as e:
        print(e)

    return JsonResponse({'orders_f_bi':all_good_orders['Binance']['Future'],
                         'orders_s_bi':all_good_orders['Binance']['Spot'],
                         'orders_f_by':all_good_orders['Bybit']['Future'],
                         'orders_s_by':all_good_orders['Bybit']['Spot'],
                           'close_levels':good_levels})


def index(request):
    return render(request, 'screener/close_three_levels.html')

def get_data(request):
    close_levels_result = get_close_three_levels()
    
    
    return JsonResponse({'close_levels':close_levels_result})


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
    deals = get_all_deals()
    chart = get_chart_equity(deals)
    
    sum_profit = 0
    good_deals = 0
    bad_deals = 0

    for deal in deals:
        profit = deal[10]

        percent = round(profit / 5 * 100,2)
        sum_profit += percent

        if percent > 0:
            good_deals += 1
        
        if percent < -0.1:
            bad_deals += 1
    
    percent_good = 0
    if len(deals) > 1:
        percent_good = good_deals / (good_deals + bad_deals) * 100

    return render(request, 'screener/positions.html', {'chart':chart,'all_profit':round(sum_profit,2),'count_deals':good_deals + bad_deals, 'percent_good':round(percent_good, 2)})

def get_data_position(request):
    result_positions = []
    result_deals = []
    try:
        positions = get_all_positions()
        
        #9 7 

        last_prices = get_all_last_prices()
        for pos in positions:
            my_list = list(pos)
            id = my_list[0]
            exchange = my_list[1]
            type_exchange = my_list[2]
            symbol = my_list[3]
            side = my_list[4]
            quantity = my_list[5]
            price_open = my_list[6]
            date_open =  my_list[7].strftime("%d/%m/%Y, %H:%M:%S")

            best_bid = last_prices[exchange][type_exchange][symbol]['best_bid']
            best_ask = last_prices[exchange][type_exchange][symbol]['best_ask']
            stop = my_list[8]
            stop_vol = my_list[9]
            tp = my_list[11]
            left_pips_stop = 0
            left_pips_take = 0
            if side == 'LONG':
                left_pips_stop = round(100 - stop / best_ask * 100,2)
                left_pips_take = round(100 - best_bid / tp * 100, 2)

            else:
                left_pips_stop = round(100 - best_bid / stop * 100,2)
                left_pips_take = round(100 - tp / best_ask * 100,2)


            result_positions.append([id, exchange, type_exchange, symbol,
                                      side, quantity,price_open, date_open,
                                        stop_vol, stop, left_pips_stop, tp, left_pips_take])

        deals = get_all_deals()
        
        

        for deal in deals:
            my_list = list(deal)
            my_list[7] =  my_list[7].strftime("%d/%m/%Y, %H:%M:%S")
            my_list[9] =  my_list[9].strftime("%d/%m/%Y, %H:%M:%S")

            profit = deal[10]

            percent = round(profit / 5 * 100,2)
            my_list[10] = percent
            result_deals.append(my_list)
    except Exception as e:
        print(e)
    return JsonResponse({'positions':result_positions, 'deals':result_deals})



def current_position(request, id):
    pos = get_position_by_id(id)
    chart = get_chart_current_position(pos)
    return render(request, 'screener/close_level.html', {'chart':chart, 'name':pos[3]})

def current_deal(request, id):
    print(id)
    deals = get_deal_by_id(int(id))
    symbol = deals[3]
    chart = get_chart_deal_rebound_level(deals)
    chart_2 = get_chart_deal_rebound_level_zoom(deals)
    return render(request, 'screener/current_deal.html', {'name':symbol,'chart':chart, 'chart_2':chart_2})
        

