import numpy as np
import datetime
import pandas as pd

def split(a, n):
    k, m = divmod(len(a), n)
    return list((a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)))

def get_max_index_list(array, period = 30):
    list_max_index = []


    i = period
    while i < array.size - period:
        high_list = array[i - period: i + period] 
        max_index = np.argmax(high_list)
        if high_list[period] == high_list[max_index]:
            list_max_index.append(i)
            i += period
        else:
            i += 1
    return list_max_index

def get_min_index_list(array, period = 30):
    list_min_index = []

    i = period
    while i < array.size - period:
        low_list = array[i - period: i + period] 
        min_index = np.argmin(low_list)
        if low_list[period] == low_list[min_index]:
            list_min_index.append(i)
            i += period
        else:
            i += 1
    return list_min_index

def get_min_max_list(df, period = 30):
    result = dict()

    result['max_list'] = get_max_index_list(np.array(df['High']),period)
    result['min_list'] = get_min_index_list(np.array(df['Low']),period)

    return result

def Extract(lst):
    return [item[4] for item in lst]

def atr(df, period):
    try:
        df['Max'] =  df['High'].rolling(period).max().shift().fillna(0)
        df['Min'] = df['Low'].rolling(period).min().shift().fillna(0)

        df['Atr'] = df['Max'] - df['Min']

        return df.drop(columns = ['Max','Min'])
    except Exception as e:
        print(e)


def impulse_short(df_HighTF, result_impulses, pulse_percent=0.2):
    impulses = []
    percent_return = 0.3
    percent_not_change = 0.3

    df_HighTF = atr(df_HighTF, period=300)
    list = df_HighTF.values.tolist()

    isDown = False
    min = 0
    max = 0
    height = 0
    curr_diff = 0
    count_trend_bar = 0
    count_after_trend_bar = 0

    priceStart = 0
    dateStart = datetime.datetime.now()
    dateEnd = datetime.datetime.now()

    supermin = 0
    supermax = 0

    for i, x in enumerate(list):
        if isDown:
            if list[i][2] < supermin:
                    supermin = list[i][2]

            if list[i][1] > supermax:
                supermax = list[i][1]
            if list[i][3] < min:
                min = list[i][3]
                height = max - min
                count_trend_bar += 1
                count_after_trend_bar = 0
                priceEnd = list[i][3]
                dateEnd = list[i][5]
                if i + 1 != len(list):
                    dateEnd = list[i + 1][5]

                
            else:
                count_after_trend_bar += 1
                curr_diff = list[i][3] - min
                if (curr_diff > height * percent_return):
                    isDown = False

                    if (height > pulse_percent * list[i][6] and count_trend_bar > 1 and list[i][6] != 0):
                        impulses.append({'price_start':supermax, 'date_start':dateStart,
                                          'price_end':supermin, 'date_end':dateEnd,
                                            'iEnd':i - count_after_trend_bar, 'is_open' : 0})
                else:
                    count_stop_bar = 0

                    if (count_trend_bar < 10):
                        count_stop_bar = 4
                    else:
                        count_stop_bar = int(count_trend_bar * percent_not_change)

                    if (count_after_trend_bar > count_stop_bar):
                        isDown = False

                        if (height > pulse_percent * list[i][6] and count_trend_bar > 1 and list[i][6] != 0):
                            impulses.append({'price_start':priceStart, 'date_start':dateStart,
                                          'price_end':supermin, 'date_end':dateEnd,
                                            'iEnd':i - count_after_trend_bar, 'is_open' : 0})
        else:
            if (list[i][3] < list[i - 1][3]):
                isDown = True
                min = list[i][0]
                max = list[i][3]
                supermin = list[i][2]
                supermax = list[i][1]
                height = max - min
                count_trend_bar = 1
                count_after_trend_bar = 0
                priceStart = list[i][0]
                dateStart = list[i][5]

    if len(impulses) != 0:
        result_impulses['Short'] = impulses[-1]


def impulse_long(df_HighTF,result_impulses, pulse_percent = 0.2):
    impulses = []
    percent_return = 0.3
    percent_not_change = 0.3


    df_HighTF = atr(df_HighTF, period = 300)
    list = df_HighTF.values.tolist()

    isUp = False
    min = 0
    max = 0
    height = 0
    curr_diff = 0
    count_trend_bar = 0
    count_after_trend_bar = 0

    priceStart = 0
    dateStart = datetime.datetime.now()
    dateEnd = datetime.datetime.now()

    supermax = 0
    supermin = 0

    for i, x in enumerate(list):
        if isUp:

            if list[i][1] > supermax:
                    supermax = list[i][1]

            if list[i][2] < supermin:
                supermin = list[i][2]
            if list[i][3] > max:
                max = list[i][3]
                height = max - min
                count_trend_bar += 1
                count_after_trend_bar = 0
                priceEnd = list[i][3]
                dateEnd = list[i][5]
                if i + 1 != len(list):
                    dateEnd = list[i + 1][5]

                
            else:
                count_after_trend_bar += 1
                curr_diff = max - list[i][3]
                if(curr_diff > height * percent_return):
                    isUp = False

                    if(height > pulse_percent * list[i][6] and count_trend_bar > 1 and list[i][6] != 0):
                        impulses.append({'price_start':supermin, 'date_start':dateStart,
                                          'price_end':supermax, 'date_end':dateEnd,
                                            'iEnd':i - count_after_trend_bar, 'is_open' : 0})
                else:
                    count_stop_bar = 0

                    if(count_trend_bar < 10):
                        count_stop_bar = 4
                    else:
                        count_stop_bar = int(count_trend_bar * percent_not_change)
                    
                    if(count_after_trend_bar > count_stop_bar):
                        isUp = False

                        if(height > pulse_percent * list[i][6] and count_trend_bar > 1 and list[i][6] != 0):
                            impulses.append({'price_start':priceStart, 'date_start':dateStart,
                                          'price_end':supermax, 'date_end':dateEnd,
                                            'iEnd':i - count_after_trend_bar, 'is_open' : 0})
        else:
            if(list[i][3] > list[i-1][3]):
                isUp = True
                min = list[i][0]
                max = list[i][3]
                supermax = list[i][1]
                supermin = list[i][2]
                height = max - min
                count_trend_bar = 1
                count_after_trend_bar = 0
                priceStart = list[i][0]
                dateStart = list[i][5]

    if len(impulses) != 0:
        result_impulses['Long'] = impulses[-1]


def get_df_from_candles(candles):
    df = pd.DataFrame(candles, columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])
    return df