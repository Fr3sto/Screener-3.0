import pandas as pd
from shared_memory_dict import SharedMemoryDict

from screener.database import get_all_currency, get_all_levels, get_all_impulses, get_all_order_book
from screener.charts import get_chart_with_impulse

def collect_data_for_levels():
    
    currency_list = get_all_currency()

    all_levels_df = pd.DataFrame(get_all_levels(), columns=['id','symbol','price','type','date'])
    result_data = dict()

    for currency in currency_list:
        symbol = currency[1]
        result_data[symbol] = dict()

        symbol_levels_df = all_levels_df[all_levels_df['symbol'] == symbol]
        
        symbol_levels_df = symbol_levels_df.sort_values(by=['price'], ascending=  False)
        
        if not symbol_levels_df.empty:
            for row in symbol_levels_df.itertuples():
                result_data[symbol][row.price] = {'type':row.type}


    return result_data

def collect_all_data_for_screener():
    currency_list = get_all_currency()
    list_tf = [5,15,30,60]

    result = dict()
    empty_res = dict()

    
    df_imp =  pd.DataFrame(get_all_impulses(), columns=['id','symbol','type','tf','price_s','date_s','price_e','date_e','is_open'])

    df_order_book = pd.DataFrame(get_all_order_book(), columns=['id','symbol','type','price','pow','quantity','is_not_mm','date_start','date_end'])
    df_order_book['date_start'] = pd.to_datetime(df_order_book['date_start'])
    df_order_book['date_end'] = pd.to_datetime(df_order_book['date_end'])
    #df_level = pd.DataFrame(get_all_levels(), columns=['id','symbol','tf','price','type','date_start'])



    # print(df_imp)
    # print(df_level)
    # print(currency_list)
    for curr in currency_list:
        result[curr[1]] = {'tf' : dict()}
        
        
        isImpulse = False
        for tf in list_tf:
            imp = df_imp[(df_imp['symbol'] == curr[1]) & (df_imp['tf'] == tf)]
            if not imp.empty:
                result[curr[1]]['tf'][tf] = {"text":"График", "type": imp['type'].iloc[0], "count_orders" : 0, 'price_start':imp['price_s'].iloc[0],
                                             'price_end':imp['price_e'].iloc[0]}
                isImpulse = True
            else:
                result[curr[1]]['tf'][tf] = {}
                
        if not isImpulse:
            empty_res[curr[1]] = result[curr[1]]
            del result[curr[1]]
    

    for symbol, tf in result.items():
        df_ob = df_order_book[(df_order_book['symbol'] == symbol) & ((df_order_book['date_end'] - df_order_book['date_start']).dt.total_seconds() / 60 > 15)]
        for tf, tf_list in tf.items():
            for tf, value in tf_list.items():
                if 'type' in value:
                    if value['type'] == 'L':
                        up_price = value['price_end']
                        up_price += up_price * 0.01

                        down_price = value['price_start']

                        df_ob = df_ob[(df_ob['price'] < up_price) & (df_ob['price'] > down_price)]
                    else:
                        up_price = value['price_start']

                        down_price = value['price_end']
                        down_price -= down_price * 0.01

                        df_ob = df_ob[(df_ob['price'] < up_price) & (df_ob['price'] > down_price)]
                    value['count_orders'] = df_ob.shape[0]
    #result.update(empty_res)
    return result

from screener.database import get_candles_by_symbol_tf, get_impulse_opened, get_levels_by_symbol_tf

def get_currency_chart_with_impulse(symbol, tf):
    candles = get_candles_by_symbol_tf(symbol, tf)
    df_candles = get_df_from_candles(candles)
    impulse = get_impulse_opened(symbol, tf)[0]
    level_list = get_levels_by_symbol_tf(symbol, tf)
    return get_chart_with_impulse(df_candles, impulse,level_list, tf,symbol)


def get_df_from_candles(candles):
    df = pd.DataFrame(candles, columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])
    return df