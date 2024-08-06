import pandas as pd
from datetime import datetime

from screener.database import get_all_impulses, get_all_levels, get_all_order_book


def collect_all_data_for_screener():
    
    list_tf = [5,15,30,60]

    result = dict()
    empty_res = dict()

    
    
    impulse_list =  get_all_impulses()

    result = dict()

    levels = get_all_levels()

    all_orders = get_all_order_book()

    for impulse in impulse_list:
        symbol = impulse[1]
        type = impulse[2]
        tf = impulse[3]
        price_start = impulse[4]
        price_end = impulse[6]

        up_price = 0
        down_price = 0

        if type == 'L':
            up_price = price_end
            up_price += up_price * 0.01

            down_price = price_start
        else:
            up_price = price_start

            down_price = price_end
            down_price -= down_price * 0.01

        count_levels = 0

        for level in levels:
            if level[1] == symbol and level[2] == tf:
                count_levels += 1


        count_orders = 0

        for order in all_orders:
            exch = order[1]
            type_exch = order[2]
            symbol_order = order[3]
            price_order = order[5]
            date_start = order[9]
            date_end = order[10]
            if symbol_order == 'LTCUSDT':
                pass
            if type_exch == 'Future':
                if symbol_order == symbol and price_order < up_price and price_order > down_price:
                    if (date_end - date_start).total_seconds() / 60 > 30:
                        count_orders += 1
            else:
                curr_symbol = symbol.split('USDT')[0] + '/USDT'
                if symbol_order == curr_symbol and price_order < up_price and price_order > down_price:
                    if (date_end - date_start).total_seconds() / 60 > 30:
                        count_orders += 1
            


        if symbol in result:
            result[symbol]['tf'][tf] = {"text":"График", "type": type, "count_orders" : count_orders, 'price_start':price_start,
                                              'price_end':price_end, 'count_levels': count_levels}
        else:
            result[symbol] = {'tf' : {tf : {"text":"График", "type": type, "count_orders" : count_orders, 'price_start':price_start,
                                              'price_end':price_end, 'count_levels': count_levels}}}
            
    for symbol, value in result.items():
        if not 5 in value['tf']:
            value['tf'][5] = {}
        if not 15 in value['tf']:
            value['tf'][15] = {}
        if not 30 in value['tf']:
            value['tf'][30] = {}
        if not 60 in value['tf']:
            value['tf'][60] = {}
        value['tf'] = dict(sorted(value['tf'].items(), key=lambda item: item[0]))


    good_result = dict()
    bad_result = dict()

    for key,value in result.items():
        is_good = True
        # is_good = False
        # for tf, value_2 in value['tf'].items():
        #     if 'count_orders' in value_2 and value_2['count_orders'] != 0:
        #         is_good = True
        #         break
        if is_good == True:
            good_result[key] = result[key]
        else:
            bad_result[key] = result[key]
    

    for key,value in bad_result.items():
        good_result[key] = bad_result[key]
    return good_result



from screener.database import get_candles_by_symbol_tf, get_impulse_opened, get_levels_by_symbol_tf, get_order_book_by_symbol

from screener.charts import get_chart_with_impulse

def get_currency_chart_with_impulse(symbol, tf, min_step):
    candles = get_candles_by_symbol_tf(symbol, tf)
    df_candles = get_df_from_candles(candles)
    impulse = get_impulse_opened(symbol, tf)[0]
    levels = get_levels_by_symbol_tf(symbol, tf)
    orders_future = get_order_book_by_symbol(symbol)
    orders_spot = get_order_book_by_symbol(symbol.split('USDT')[0] + '/USDT')
    return get_chart_with_impulse(df_candles, impulse,levels,orders_future,orders_spot, tf,symbol, min_step)


def get_df_from_candles(candles):
    df = pd.DataFrame(candles, columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])
    return df