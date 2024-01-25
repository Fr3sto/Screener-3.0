from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import ccxt


from screener.database import  (get_all_positions,get_all_currency,
                                 get_close_levels, get_all_deals, 
                                 get_deal_by_id, get_all_levels, get_all_status_check, get_all_order_books, get_all_symbols_for_order_book)
from screener.charts import ( get_chart_deal_break_level, get_chart_deal_rebound_level, get_chart_deal_rebound_level_zoom,
                              get_chart_deal_break_level_zoom, get_chart_close_levels,
                                get_chart_three_close_level,get_chart_two_close_level, get_chart_equity,
                                get_chart_current_position)

from screener.exchange import get_all_last_prices

from screener.services import get_close_three_levels, get_close_two_levels


def big_orders(request):
    return render(request, 'screener/big_orders.html')

all_currency = get_all_symbols_for_order_book()

binance = ccxt.binance()

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
                    if symbol in all_currency[exchange][type_exchange] and symbol in last_prices[exchange][type_exchange]:
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

        # levels = get_all_levels()
        # for level in levels:
        #     symbol = level[1]
        #     price = level[3]
        #     type = level[4]
        #     date_start = level[5]
        #     time_live_level = (datetime.now() - date_start).seconds / 60
        #     last_price = last_prices[symbol]['last_price']

        #     left_pips = 0
        #     if type == 1:
        #         left_pips = 100 - last_price / price * 100
        #         if left_pips < 2:
        #             for price_order, order in order_book[symbol]['asks'].items():
        #                 if price_order >= price:
        #                     order_count_decimal = str(round(price_order / curr_list[symbol]['min_step']))
        #                     if order_count_decimal[-1] == '0':
        #                         left_pips_order_level = 100 - price / price_order * 100
        #                         if left_pips_order_level < 0.5 and order['is_not_mm'] == True:
        #                             left_pips_order = 100 - last_price / price_order * 100
        #                             time_live = (order['date_end'] - order['date_start']).seconds / 60
        #                             good_levels.append((type, symbol, price,round(time_live_level), round(left_pips,2), price_order, order['pow'],round(time_live), round(left_pips_order,2)))
        #     else:
        #         left_pips = 100 - price / last_price * 100
        #         if left_pips < 2:
        #             for price_order, order in order_book[symbol]['bids'].items():
        #                 if price_order <= price:
        #                     order_count_decimal = str(round(price_order / curr_list[symbol]['min_step']))
        #                     if order_count_decimal[-1] == '0':
        #                         left_pips_order_level = 100 - price_order / price * 100
        #                         if left_pips_order_level < 0.5 and order['is_not_mm'] == True:
        #                             left_pips_order = 100 - price_order / last_price * 100
        #                             time_live = (order['date_end'] - order['date_start']).seconds / 60
        #                             good_levels.append((type, symbol, price,round(time_live_level), round(left_pips,2), price_order, order['pow'],round(time_live), round(left_pips_order,2)))
            

        # good_levels = sorted(good_levels, key=lambda x: x[4])
            

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

def chart_close_level(request, symbol, level):
    chart = get_chart_three_close_level(symbol, level)
    return render(request, 'screener/close_level.html', {'chart':chart, 'name':symbol})


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

    all_deals = []
    for deal in deals:
        if deal[2] == 'rebound_level':
            side = deal[3]
            quantity = deal[4]
            price_open = deal[5]
            date_open = deal[6]
            price_close = deal[7]
            profit = deal[9]

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
        

        for pos in positions:
            my_list = list(pos)
            my_list[6] =  my_list[6].strftime("%d/%m/%Y, %H:%M:%S")
            result_positions.append(my_list)

        deals = get_all_deals()
        
        

        for deal in deals:
            my_list = list(deal)
            my_list[6] =  my_list[6].strftime("%d/%m/%Y, %H:%M:%S")
            my_list[8] =  my_list[8].strftime("%d/%m/%Y, %H:%M:%S")

            side = deal[3]
            quantity = deal[4]
            price_open = deal[5]
            price_close = deal[7]
            profit = deal[9]

            percent = round(profit / 5 * 100,2)
            my_list[9] = percent
            result_deals.append(my_list)
    except Exception as e:
        print(e)
    return JsonResponse({'positions':result_positions, 'deals':result_deals})

def current_position(request, symbol):
    chart = get_chart_current_position(symbol)
    return render(request, 'screener/close_level.html', {'chart':chart, 'name':symbol})

def current_deal(request, id):
    print(id)
    deals = get_deal_by_id(int(id))
    symbol = deals[0][1]
    strategy = deals[0][2]
    if strategy == 'break_level':
        chart = get_chart_deal_break_level(deals[0])
        chart_2 = get_chart_deal_break_level_zoom(deals[0])
        return render(request, 'screener/current_deal.html', {'name':symbol,'chart':chart, 'chart_2':chart_2})
    elif strategy == 'rebound_level':
        chart = get_chart_deal_rebound_level(deals[0])
        chart_2 = get_chart_deal_rebound_level_zoom(deals[0])
        return render(request, 'screener/current_deal.html', {'name':symbol,'chart':chart, 'chart_2':chart_2})

