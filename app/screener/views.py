from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
import ccxt
import pandas as pd

from screener.services import collect_all_data_for_screener

from screener.database import get_status, get_all_currency

from screener.exchange import get_last_prices, get_all_min_step, get_candles_by_date

from screener.charts import chart_with_flat


currency_list = get_all_currency()

def index(request):

    try:
        print('Good')
        data = collect_all_data_for_screener()
        list_tf = [5,15,30,60]

        return render(request, 'screener/index.html', {'data':data, 'list_tf':list_tf})
    except Exception as e:
        print(e)

from screener.services import get_currency_chart_with_impulse

def currency_chart(request, symbol, tf):
    print(symbol, tf)
    chart = get_currency_chart_with_impulse(symbol,tf)
    return render(request, 'screener/currency_chart.html', {'chart':chart})




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