import pandas as pd
from threading import Thread

from calculations.other_func import impulse_long, impulse_short
from calculations.database import get_candles_by_symbol_tf, insert_impulse, get_all_impulses, get_impulses_by_tf, delete_impulse
from calculations.other_func import get_df_from_candles

def calculate_all_impulses_by_tf(tf, high_tf, currency_list,opened_impulses = pd.DataFrame(columns=['symbol'])):
    impulse_percent = 0.2
    for currency in currency_list:
        if opened_impulses[opened_impulses['symbol'] == currency].empty:
            candles =  get_candles_by_symbol_tf(currency, high_tf)
            df = get_df_from_candles(candles)
            result_impulses = dict()
            result_impulses['Long'] = {}
            result_impulses['Short'] = {}
            impulse_long(df,result_impulses)
            impulse_short(df,result_impulses)

            if result_impulses['Long'] | result_impulses['Short']:
                candles_curr =  get_candles_by_symbol_tf(currency, tf)
                df_curr = get_df_from_candles(candles_curr)
                check_is_opened_impulse(df_curr, result_impulses)

                if result_impulses['Long']:
                    insert_impulse(currency, 'L', tf, result_impulses['Long'])
                if result_impulses['Short']:
                    insert_impulse(currency, 'S', tf, result_impulses['Short'])
    print(f"Impulses {tf} done")


def calculate_impulses(currency_list, list_tf):


    opened_impulses = pd.DataFrame(get_all_impulses(), columns=['id','symbol','type','tf','price_s','date_s','price_e','date_e','is_open'])

    threads = []
    for tf in list_tf:
        high_tf = 0

        match tf:
            case 5:
                high_tf = 15
            case 15:
                high_tf = 60
            case 30:
                high_tf = 120
            case 60:
                high_tf = 240

        
        if opened_impulses.size != 0:
            th = Thread(target=calculate_all_impulses_by_tf, args=(tf,high_tf,currency_list,opened_impulses[opened_impulses['tf'] == tf]))
            threads.append(th)
        else:
            th = Thread(target=calculate_all_impulses_by_tf, args=(tf,high_tf,currency_list))
            threads.append(th)

    for x in threads:
        x.start()

    for x in threads:
        x.join()

    
def check_is_opened_impulse(df, result_impulses):
    pulse_return = 0.5
    # Для лонга
    first_date = df['Date'].iloc[0]
    if result_impulses['Long']:
        if first_date < result_impulses['Long']['date_end']:
            max_pulse = result_impulses['Long']['price_end']
            min_pulse = result_impulses['Long']['price_start']
            df_res = df[(df['Date'] >= result_impulses['Long']['date_end']) & ((df['Close'] > max_pulse) | (df['Close'] < max_pulse - (max_pulse - min_pulse) * pulse_return))]
            if df_res.empty:
                result_impulses['Long']['is_open'] = 1
            else:
                result_impulses['Long'] = {}
        else:
            result_impulses['Long'] = {}

    # Для шорта

    if result_impulses['Short']:
        if first_date < result_impulses['Short']['date_end']:
            max_pulse = result_impulses['Short']['price_start']
            min_pulse = result_impulses['Short']['price_end']
            df_res = df[(df['Date'] >= result_impulses['Short']['date_end']) & ((df['Close'] < min_pulse) | (df['Close'] > min_pulse + (max_pulse - min_pulse) * pulse_return))]
            if df_res.empty:
                result_impulses['Short']['is_open'] = 1
            else:
                result_impulses['Short'] = {}
        else:
            result_impulses['Short'] = {}

def check_impulse_end(list_TF, result_candles):
    
    for TF in list_TF:
        opened_impulses_list = get_impulses_by_tf(TF)

        for impulse in opened_impulses_list:
            symbol = impulse[1]
            type = impulse[2]
            tf = impulse[3]
            price_end = impulse[6]
            price_start = impulse[4]
            candle = result_candles[str(symbol) + '-' + str(tf)]
            close = candle[0][4]
            if type == "L":
                if close > price_end and close < (price_end - (price_end - price_start) * 0.5):
                    delete_impulse(symbol, tf)

            if type == "S":
                if close < price_end and close > (price_end + (price_start - price_end) * 0.5):
                    delete_impulse(symbol, tf)

    