from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime


from screener.database import  (get_all_positions,get_all_currency,
                                 get_close_levels, get_all_deals, 
                                 get_deal_by_id, get_all_levels, get_all_status_check)
from screener.charts import ( get_chart_deal,
                              get_chart_deal_zoom, get_chart_close_levels,
                                get_chart_three_close_level,get_chart_two_close_level, get_chart_equity,
                                get_chart_current_position)

from screener.exchange import  get_last_prices_f

from screener.services import get_close_three_levels, get_close_two_levels

def index(request):
    return render(request, 'screener/close_three_levels.html')

def get_data(request):
    close_levels_result = get_close_three_levels()
    
    
    return JsonResponse({'close_levels':close_levels_result})


curr_list = get_all_currency()

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

def current_position(request, symbol):
    chart = get_chart_current_position(symbol)
    return render(request, 'screener/close_level.html', {'chart':chart, 'name':symbol})

def current_deal(request, id):
    print(id)
    deals = get_deal_by_id(int(id))
    symbol = deals[0][1]
    chart = get_chart_deal(deals[0])
    chart_2 = get_chart_deal_zoom(deals[0])
    return render(request, 'screener/current_deal.html', {'name':symbol,'chart':chart, 'chart_2':chart_2})

