import pandas as pd

from screener.database import get_all_currency, get_all_impulses, get_all_order_book
from screener.charts import get_chart_with_impulse


def collect_all_data_for_screener(currency_list):
    
    list_tf = [5,15,30,60]

    result = dict()
    empty_res = dict()

    
    impulse_list =  get_all_impulses()

    order_book_list = get_all_order_book()
    
    order_book = dict()

    for symbol in currency_list:
        order_book[symbol[1]] = []

    for order in order_book_list:
        symbol = order[1]
        type = order[2]
        price = order[3]
        order_book[symbol].append(price)

    result = dict()

    orders_prices_symbol = dict()
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

        
        count_orders = 0

        if symbol in orders_prices_symbol:
            count_orders = orders_prices_symbol[symbol]
        else:
            for price in order_book[symbol]:
                if price < up_price and price > down_price:
                    count_orders += 1
            orders_prices_symbol[symbol] = count_orders
        

        if symbol in result:
            result[symbol]['tf'][tf] = {"text":"График", "type": type, "count_orders" : 0, 'price_start':price_start,
                                              'price_end':price_end, 'count_orders':count_orders}
        else:
            result[symbol] = {'tf' : {tf : {"text":"График", "type": type, "count_orders" : 0, 'price_start':price_start,
                                              'price_end':price_end, 'count_orders':count_orders}}}
            
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

    return result

from screener.database import get_candles_by_symbol_tf, get_impulse_opened

def get_currency_chart_with_impulse(symbol, tf):
    candles = get_candles_by_symbol_tf(symbol, tf)
    df_candles = get_df_from_candles(candles)
    impulse = get_impulse_opened(symbol, tf)[0]
    return get_chart_with_impulse(df_candles, impulse, tf,symbol)


def get_df_from_candles(candles):
    df = pd.DataFrame(candles, columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])
    return df