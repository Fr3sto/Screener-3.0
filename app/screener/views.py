from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime


from screener.database import  (get_all_positions,get_all_currency,
                                 get_close_levels, get_all_deals, 
                                 get_deal_by_id, get_all_levels, get_all_status_check)
from screener.charts import ( get_chart_deal,
                              get_chart_deal_zoom, get_chart_close_levels,
                                get_chart_close_level, get_chart_equity)

from screener.exchange import  get_last_prices_f, get_currencies

currency_list = get_all_currency()

def index(request):
    return render(request, 'screener/close_levels.html')

def get_data(request):
    close_levels_result = []
    last_prices = get_last_prices_f()
    try:
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
    
    
    return JsonResponse({'close_levels':close_levels_result})


curr_list = get_currencies(100)

def chart_close_level(request, symbol, level):
    chart = get_chart_close_level(symbol, level)
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
    for deal in deals:
        side = deal[2]
        quantity = deal[3]
        price_open = deal[4]
        price_close = deal[6]
        profit = deal[8]

        if profit > 0:
            profit += price_open * quantity * 0.00025
            profit += price_close * quantity * 0.00025

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
            my_list[5] =  my_list[5].strftime("%d/%m/%Y, %H:%M:%S")
            result_positions.append(my_list)

        deals = get_all_deals()
        
        

        for deal in deals:
            my_list = list(deal)
            my_list[5] =  my_list[5].strftime("%d/%m/%Y, %H:%M:%S")
            my_list[7] =  my_list[7].strftime("%d/%m/%Y, %H:%M:%S")

            side = deal[2]
            quantity = deal[3]
            price_open = deal[4]
            price_close = deal[6]
            profit = deal[8]

            percent = round(profit / 5 * 100,2)
            my_list[8] = percent
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

