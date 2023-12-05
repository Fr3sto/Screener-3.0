import pandas as pd
from threading import Thread

from other_func import split, get_min_max_list
from database import (get_all_levels,delete_level, get_candles_by_symbol_tf, get_all_impulses, insert_levels, get_levels_by_tf,
                      delete_closed_level)

def calculate_all_levels_after_impulse_by_tf(tf, impulses : pd.DataFrame):
    level_period = 20

    result = dict()

    for impulse in impulses.itertuples():
        result[impulse.symbol] = dict()
        candles_df = pd.DataFrame(get_candles_by_symbol_tf(impulse.symbol, tf), columns=['id','Symbol','TF','Open','High','Low','Close','Volume','Date'])
        candles_df = candles_df[candles_df['Date'] >= impulse.date_end]
        dict_min_max = get_min_max_list(candles_df,level_period)

        max_list = []
        for el in dict_min_max['max_list']:
            max_list.append((candles_df['High'].values[el], candles_df['Date'].iloc[el]))
        
        for el in max_list:
            df_res = candles_df[(candles_df['Date'] >= el[1]) & (candles_df['High'] > el[0])]
            if df_res.empty:
                result[impulse.symbol][el[1]] = {'price': el[0], 'type' : 1, 'date_start':el[1]}
                    

        min_list = []
        for el in dict_min_max['min_list']:
            min_list.append((candles_df['Low'].values[el],candles_df['Date'].iloc[el] ))

        for el in min_list:
            df_res = candles_df[(candles_df['Date'] >= el[1]) & (candles_df['Low'] < el[0])]
            if df_res.empty:
                result[impulse.symbol][el[1]] = {'price': el[0], 'type' : 2, 'date_start':el[1] }

    insert_levels(result, tf)


def calculate_levels_after_impulse(list_TF):

    opened_impulses = pd.DataFrame(get_all_impulses(), columns=['id','symbol','type','tf','price_start','date_start','price_end','date_end','is_open'])

    threads = []
    for tf in list_TF:
        if not opened_impulses[opened_impulses['tf'] == tf].empty:
            th = Thread(target=calculate_all_levels_after_impulse_by_tf, args=(tf,opened_impulses[opened_impulses['tf'] == tf]))
            threads.append(th)
    
    for x in threads:
        x.start()

    for x in threads:
        x.join()

def check_level_end(list_TF, result_candles):
    
    for TF in list_TF:
        levels_list = get_levels_by_tf(TF)

        for level in levels_list:
            symbol = level[1]
            candle = result_candles[str(symbol) + '-' + str(level[2])]
            close = candle[0][4]
            if level[4] == 1:
                if close > level[3]:
                    delete_closed_level(symbol, level[2], level[5])

            if level[4] == -1:
                if close < level[3]:
                    delete_closed_level(symbol, level[2], level[5])