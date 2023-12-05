from threading import Thread
from multiprocessing import Process, Pool
import requests
import time
from datetime import datetime

from calculations.database import delete_all_candles, insert_candles_bulk, delete_all_levels
from calculations.exchange import get_klines,get_kline
from calculations.other_func import split
from calculations.impulses import check_impulse_end, calculate_impulses
from calculations.levels import check_level_end,calculate_levels_after_impulse

TF_list = ['5m','15m','30m','1h','2h','4h']
TF_list_num = [5,15,30,60,120,240]

def get_start_candles(currency_dict : dict):
    print("Start candles getting now")

    delete_all_candles()

    print('Old candles deleted')

    currency_list = split(list(currency_dict.keys()), 3)
    
    partI = 0

    result = dict()
    for part in currency_list:
        
        threads = []
        for index, TF in enumerate(TF_list):
            th = Thread(target = get_klines, args=(result,part,TF,TF_list_num[index], 500))
            threads.append(th)
        
        for th in threads:
            th.start()

        for th in threads:
            th.join()

        print('End part ',partI)
        partI += 1 

    insert_candles_bulk(result)

    print("Start candles inserted")
    
def get_last_candles_and_impulse(currency_dict, last_minute, last_hour):
    currency_list_part = split(list(currency_dict.keys()),5)

    print("Get last Candles")
    result_list = dict()
    threads = list()

    list_TF = []

    if last_minute % 5 == 0:
        th5 = Thread(target=get_kline, args=(result_list,currency_dict,'5m', 5))
        threads.append(th5)
        list_TF.append(5)
        
    if last_minute % 15 == 0:
        th15 = Thread(target=get_kline, args=(result_list,currency_dict,'15m', 15))
        threads.append(th15)
        list_TF.append(15)

    if last_minute % 30 == 0:
        th30 = Thread(target=get_kline, args=(result_list,currency_dict,'30m', 30))
        threads.append(th30)
        list_TF.append(30)

    if last_minute == 0:
        th60 = Thread(target=get_kline, args=(result_list,currency_dict,'1h', 60))
        threads.append(th60)
        list_TF.append(60)

    if last_minute == 0 and (last_hour + 1) % 2 == 0:
        th120 = Thread(target=get_kline, args=(result_list,currency_dict,'2h', 120))
        threads.append(th120)

    if last_minute == 0 and (last_hour + 1) % 4 == 0:
        th240 = Thread(target=get_kline, args=(result_list,currency_dict,'4h', 240))
        threads.append(th240)
    
    for th in threads:
        th.start()

    for th in threads:
        th.join()

    insert_candles_bulk(result_list)
    print("Got last Candles")


    #Дальше мы должны рассчитать все наши индкаторы
    if len(list_TF) != 0:
        # Проверить, из каких импульсов мы вышли после новых свеч
        print('Check impulse end')
        check_impulse_end(list_TF,result_list)
        print('Check level end')
        check_level_end(list_TF,result_list)
        # Какие ТФ прошли, по ним высчитываем импульсы
        print('Calculate impulses')
        calculate_impulses(currency_dict, list_TF)
        print('Calculate levels')
        delete_all_levels()
        calculate_levels_after_impulse(list_TF)

