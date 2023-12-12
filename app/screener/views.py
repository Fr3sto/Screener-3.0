from django.shortcuts import render
from django.http import JsonResponse


from screener.services import collect_all_data_for_screener
from screener.database import  get_all_positions,get_all_currency, get_all_order_book
from screener.charts import get_order_book_chart

from screener.exchange import get_last_prices, get_currencies

currency_list = get_all_currency()

def index(request):

    try:
        print('Good')
        data = collect_all_data_for_screener(currency_list)
        list_tf = [5,15,30,60]

        return render(request, 'screener/index.html', {'data':data, 'list_tf':list_tf})
    except Exception as e:
        print(e)

def big_orders(request):
    return render(request, 'screener/big_orders.html')

curr_list = get_currencies(100)

def get_data(request):

    # positions = get_all_positions()

    # res_positions = []
    # for pos in positions:
    #     my_list = list(pos)
    #     my_list[4] = my_list[4].strftime("%H:%M:%S %d/%m/%Y")
    #     res_positions.append(my_list)

    # positions = res_positions
    good_orders = []
    positions = []
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
        for symbol, order_book in order_book.items():
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
    except Exception as e:
        print(e)
    
    
    return JsonResponse({'positions':positions, 'orders':good_orders})

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



