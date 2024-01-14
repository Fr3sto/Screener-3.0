import pandas as pd
from datetime import datetime

from screener.database import get_all_currency, get_all_levels

from screener.exchange import get_last_prices_f


def get_close_three_levels():

    close_levels_result = []
    last_prices = get_last_prices_f()

    levels = get_all_levels()

    levels_dict = dict()

    for level in levels:
        symbol = level[1]
        price = level[3]
        type = level[4]
        date_start = level[5]

        if not symbol in levels_dict:
            levels_dict[symbol] = {1 : [], 2 : []}

        levels_dict[symbol][type].append((price, date_start))
    
    for symbol, type in levels_dict.items():
        levels_1 = sorted(type[1], key=lambda x: x[0], reverse=True)

        if len(levels_1) > 2:
            for i in range(2, len(levels_1)):
                left_1 = 100 - levels_1[i][0] / levels_1[i - 1][0] * 100
                left_2 = 100 - levels_1[i][0] / levels_1[i - 2][0] * 100
                if left_1 < 0.3 and left_2 < 0.3:
                    #print(f"{symbol} Close levels Up {levels_1[i][0]} {levels_1[i - 1][0]} {levels_1[i - 2][0]}")
                    best_ask = last_prices[symbol]['best_ask']
                    left_pips = round(100 - best_ask / levels_1[i][0] * 100, 2)
                    close_levels_result.append((symbol, 1, levels_1[i][0], levels_1[i -1][0], levels_1[i - 2][0], left_pips))
                

        
        levels_2 = sorted(type[2], key=lambda x: x[0], reverse=True)

        if len(levels_2) > 2:
            for i in range(2, len(levels_2)):
                left_1 = 100 - levels_2[i][0] / levels_2[i - 1][0] * 100
                left_2 = 100 - levels_2[i][0] / levels_2[i - 2][0] * 100
                if left_1 < 0.3 and left_2 < 0.3:
                    #print(f"{symbol} Close levels Down {levels_2[i][0]} {levels_2[i - 1][0]} {levels_2[i - 2][0]}")
                    best_bid = last_prices[symbol]['best_bid']
                    left_pips = round(100 - levels_2[i - 2][0] / best_bid * 100, 2)
                    close_levels_result.append((symbol, 2, levels_2[i][0], levels_2[i -1][0], levels_2[i - 2][0], left_pips))
                

    close_levels_result = sorted(close_levels_result, key=lambda x: x[5])

    return close_levels_result

def get_close_two_levels():
    close_levels_result = []
    last_prices = get_last_prices_f()
    now = datetime.now()

    levels = get_all_levels()

    levels_dict = dict()

    for level in levels:
        symbol = level[1]
        price = level[3]
        type = level[4]
        date_start = level[5]

        if not symbol in levels_dict:
            levels_dict[symbol] = {1 : [], 2 : []}

        levels_dict[symbol][type].append((price, date_start))
    
    for symbol, type in levels_dict.items():
        levels_1 = sorted(type[1], key=lambda x: x[0], reverse=True)

        if len(levels_1) > 1:
            for i in range(1, len(levels_1)):
                left_1 = 100 - levels_1[i][0] / levels_1[i - 1][0] * 100
                time_delta = (now - levels_1[i-1][1]).seconds / 60
                if left_1 < 0.3 and time_delta > 1000:
                    #print(f"{symbol} Close levels Up {levels_1[i][0]} {levels_1[i - 1][0]} {levels_1[i - 2][0]}")
                    best_ask = last_prices[symbol]['best_ask']
                    left_pips = round(100 - best_ask / levels_1[i][0] * 100, 2)
                    close_levels_result.append((symbol, 1, levels_1[i][0], levels_1[i -1][0], left_pips))
                

        
        levels_2 = sorted(type[2], key=lambda x: x[0], reverse=True)

        if len(levels_2) > 1:
            for i in range(1, len(levels_2)):
                left_1 = 100 - levels_2[i][0] / levels_2[i - 1][0] * 100
                time_delta = (now - levels_2[i][1]).seconds / 60
                if left_1 < 0.3 and time_delta > 1000:
                    #print(f"{symbol} Close levels Down {levels_2[i][0]} {levels_2[i - 1][0]} {levels_2[i - 2][0]}")
                    best_bid = last_prices[symbol]['best_bid']
                    left_pips = round(100 - levels_2[i - 1][0] / best_bid * 100, 2)
                    close_levels_result.append((symbol, 2, levels_2[i][0], levels_2[i -1][0], left_pips))
                

    close_levels_result = sorted(close_levels_result, key=lambda x: x[4])

    return close_levels_result


def get_df_from_candles(candles):
    df = pd.DataFrame(candles, columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])
    return df