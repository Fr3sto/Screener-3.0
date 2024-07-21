from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
import ccxt
import pandas as pd

from screener.database import get_status, get_all_flat, get_flat_by_id

from screener.exchange import get_last_prices, get_all_min_step, get_candles_by_date

from screener.charts import chart_with_flat

def index(request):
    return render(request, 'screener/all_flats.html')

def get_data_flat(request):
    try:
        all_flats = get_all_flat()
        last_prices = get_last_prices()
        good_flats = []

        all_currency = get_all_min_step()

        now = datetime.now()

        for flat in all_flats:
            id = flat[0]
            symbol = flat[1]
            tf = flat[2]
            side_flat = flat[3]
            up_range = flat[8]
            down_range = flat[9]
            count_retest = flat[10]
            date_last_retest = flat[11]
            date_end = flat[7]
            best_bid = last_prices[symbol]['best_bid']
            best_ask = last_prices[symbol]['best_ask']
            left_pips = 0
            if side_flat == 1:
                price = up_range
                left_pips = 100 - price / best_bid * 100
            else:
                price = down_range
                left_pips = 100 - best_ask / price * 100

            if left_pips < 10:
                time_live = round((datetime.now() - date_end).total_seconds() / 60)
                time_last_retest = round((now - date_last_retest).total_seconds() / 60)
                good_flats.append([id,symbol,tf,side_flat,count_retest,time_last_retest, round(left_pips,2)])

        good_flats = sorted(good_flats, key=lambda x: x[5])


        return JsonResponse({'flats':good_flats})
            
    except Exception as e:
        print(e)

def current_flat(request, id):
    flat = get_flat_by_id(id)

    flat = flat[0]
    tf = flat[2]
    date_start = flat[6] - timedelta(days=1)
    now = datetime.now()
    df_candles = get_candles_by_date(flat[1], date_start, now)

    if tf == 240:
        df_candles = df_candles.groupby([df_candles['Date'].dt.floor('4H')]).agg({'Open' : 'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).reset_index()
    if tf == 60:
        df_candles = df_candles.groupby([df_candles['Date'].dt.floor('H')]).agg({'Open' : 'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).reset_index()
    else:
        df_candles = df_candles.groupby([df_candles['Date'].dt.floor(str(tf) + 'T')]).agg({'Open' : 'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).reset_index()

    chart = chart_with_flat(df_candles, flat)

    return render(request, 'screener/current_flat.html', {'name':flat[1],'chart':chart}) 


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