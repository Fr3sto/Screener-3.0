import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime

from screener.database import (get_candles_by_symbol, get_order_book_by_symbol_s, 
                               get_candles_by_symbol_tf, get_order_book_by_symbol_f, get_level_by_id,
                               get_all_levels)

def get_data_from_file(symbol):
    df_data = pd.read_csv("data/" + symbol + ".txt", sep=';', names=['Date','Level','Best_bid', 'Best_ask','Type'])
    return df_data

def get_orders_from_file(symbol):
    df_orders = pd.read_csv("orders/" + symbol + ".txt", sep=';', names=['Price','Pow','Date_Start', 'Date_End','Type','Ex'])
    return df_orders

def get_deals_from_file(symbol):
    df_orders = pd.read_csv("deals/" + symbol + ".txt", sep=';', names=['Now','Price_Level','Price_Open','Stop', 'Pow','Quantity','Date_Start','Date_End','Type'])
    return df_orders

def get_signal_from_file(symbol):
    df_orders = pd.read_csv("signal_order/" + symbol + ".txt", sep=';', names=['Now','Price_Open','Stop', 'Pow','Quantity','Date_Start','Date_End','Type'])
    return df_orders


def get_order_book_chart(symbol):

    try:
        df_candles = pd.DataFrame(get_candles_by_symbol(symbol), columns=['id','Symbol','Open','High','Low','Close','Volume','Date'])

        fig = go.Figure(data=[go.Candlestick(x=df_candles['Date'],
                                                open=df_candles['Open'], high=df_candles['High'],
                                                low=df_candles['Low'], close=df_candles['Close'])])


        fig.update_layout(xaxis_rangeslider_visible=False)

        df_deals = get_signal_from_file(symbol)
        df_deals['Now'] = pd.to_datetime(df_deals['Now'])
        df_deals['Date_Start'] = pd.to_datetime(df_deals['Date_Start'])
        df_deals['Date_End'] = pd.to_datetime(df_deals['Date_End'])
        listX_deals = []
        listY_deals = []
        list_exhange = []
        listY_stops = []

        for index, rowO in df_deals.iterrows():
            listX_deals.append(rowO['Now'])
            listY_deals.append(rowO['Price_Open'])
            listY_stops.append(rowO['Stop'])
            list_exhange.append(str(rowO['Pow']) + ' ' + str((rowO['Date_End'] - rowO['Date_Start']).seconds / 60) + ' min')

        fig.add_scatter(x = listX_deals, y = listY_deals, text=list_exhange, mode='markers', marker=dict(size=10, color="Blue"))
        fig.add_scatter(x = listX_deals, y = listY_stops,text=list_exhange, mode='markers', marker=dict(size=10, color="Red"))

        return {'fig':fig.to_html(), 'symbol':symbol}
    except Exception as e:
        print(symbol, e)


def get_chart_close_level(levels_symbol):
    
    levels = get_all_levels()

    levels_dict = dict()

    for level in levels:
        symbol = level[1]
        if symbol != levels_symbol:
            continue
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
                    left_1 = abs(100 - levels_1[i][0] / levels_1[i - 1][0] * 100)
                    left_2 = abs(100 - levels_1[i][0] / levels_1[i - 2][0] * 100)
                    if left_1 < 0.3 and left_2 < 0.3:
                        print(f"{symbol} Close levels Up {levels_1[i][0]} {levels_1[i - 1][0]} {levels_1[i - 2][0]}")
                        df = pd.DataFrame(get_candles_by_symbol_tf(symbol, 5), columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
                        df = df.drop(['id','symbol','tf'],axis=1)
                        df = df.sort_values(by=['Date'])

                        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                            open=df['Open'], high=df['High'],
                                            low=df['Low'], close=df['Close'])])
        
                        fig.update_layout(xaxis_rangeslider_visible=False)

                        fig.add_shape(type="line",
                            x0=levels_1[i][1], y0=levels_1[i][0], x1=df['Date'].iloc[-1], y1=levels_1[i][0],
                            line=dict(color='Red', width=3))
                        
                        fig.add_shape(type="line",
                            x0=levels_1[i - 1][1], y0=levels_1[i - 1][0], x1=df['Date'].iloc[-1], y1=levels_1[i - 1][0],
                            line=dict(color='Red', width=3))
                        
                        fig.add_shape(type="line",
                            x0=levels_1[i - 2][1], y0=levels_1[i - 2][0], x1=df['Date'].iloc[-1], y1=levels_1[i - 2][0],
                            line=dict(color='Red', width=3))

                        return fig.to_html()


            
            levels_2 = sorted(type[2], key=lambda x: x[0], reverse=True)

            if len(levels_2) > 2:
                for i in range(2, len(levels_2)):
                    left_1 = abs(100 - levels_2[i][0] / levels_2[i - 1][0] * 100)
                    left_2 = abs(100 - levels_2[i][0] / levels_2[i - 2][0] * 100)
                    if left_1 < 0.3 and left_2 < 0.3:
                        print(f"{symbol} Close levels Down {levels_2[i][0]} {levels_2[i - 1][0]} {levels_2[i - 2][0]}")
                        df = pd.DataFrame(get_candles_by_symbol_tf(symbol, 5), columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
                        df = df.drop(['id','symbol','tf'],axis=1)
                        df = df.sort_values(by=['Date'])

                        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                            open=df['Open'], high=df['High'],
                                            low=df['Low'], close=df['Close'])])
        
                        fig.update_layout(xaxis_rangeslider_visible=False)

                        fig.add_shape(type="line",
                            x0=levels_2[i][1], y0=levels_2[i][0], x1=df['Date'].iloc[-1], y1=levels_2[i][0],
                            line=dict(color='Green', width=3))
                        
                        fig.add_shape(type="line",
                            x0=levels_2[i - 1][1], y0=levels_2[i - 1][0], x1=df['Date'].iloc[-1], y1=levels_2[i - 1][0],
                            line=dict(color='Green', width=3))
                        
                        fig.add_shape(type="line",
                            x0=levels_2[i - 2][1], y0=levels_2[i - 2][0], x1=df['Date'].iloc[-1], y1=levels_2[i - 2][0],
                            line=dict(color='Green', width=3))

                        return fig.to_html()

def get_chart_close_levels():


    charts = []
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
                left_1 = abs(100 - levels_1[i][0] / levels_1[i - 1][0] * 100)
                left_2 = abs(100 - levels_1[i][0] / levels_1[i - 2][0] * 100)
                if left_1 < 0.3 and left_2 < 0.3:
                    print(f"{symbol} Close levels Up {levels_1[i][0]} {levels_1[i - 1][0]} {levels_1[i - 2][0]}")
                    df = pd.DataFrame(get_candles_by_symbol_tf(symbol, 5), columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
                    df = df.drop(['id','symbol','tf'],axis=1)
                    df = df.sort_values(by=['Date'])

                    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
                    fig.update_layout(xaxis_rangeslider_visible=False)

                    fig.add_shape(type="line",
                        x0=levels_1[i][1], y0=levels_1[i][0], x1=df['Date'].iloc[-1], y1=levels_1[i][0],
                        line=dict(color='Red', width=3))
                    
                    fig.add_shape(type="line",
                        x0=levels_1[i - 1][1], y0=levels_1[i - 1][0], x1=df['Date'].iloc[-1], y1=levels_1[i - 1][0],
                        line=dict(color='Red', width=3))
                    
                    fig.add_shape(type="line",
                        x0=levels_1[i - 2][1], y0=levels_1[i - 2][0], x1=df['Date'].iloc[-1], y1=levels_1[i - 2][0],
                        line=dict(color='Red', width=3))

                    charts.append({'fig':fig.to_html(), 'symbol':symbol})

        
        levels_2 = sorted(type[2], key=lambda x: x[0], reverse=True)

        if len(levels_2) > 2:
            for i in range(2, len(levels_2)):
                left_1 = abs(100 - levels_2[i][0] / levels_2[i - 1][0] * 100)
                left_2 = abs(100 - levels_2[i][0] / levels_2[i - 2][0] * 100)
                if left_1 < 0.3 and left_2 < 0.3:
                    print(f"{symbol} Close levels Down {levels_2[i][0]} {levels_2[i - 1][0]} {levels_2[i - 2][0]}")
                    df = pd.DataFrame(get_candles_by_symbol_tf(symbol, 5), columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
                    df = df.drop(['id','symbol','tf'],axis=1)
                    df = df.sort_values(by=['Date'])

                    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
                    fig.update_layout(xaxis_rangeslider_visible=False)

                    fig.add_shape(type="line",
                        x0=levels_2[i][1], y0=levels_2[i][0], x1=df['Date'].iloc[-1], y1=levels_2[i][0],
                        line=dict(color='Green', width=3))
                    
                    fig.add_shape(type="line",
                        x0=levels_2[i - 1][1], y0=levels_2[i - 1][0], x1=df['Date'].iloc[-1], y1=levels_2[i - 1][0],
                        line=dict(color='Green', width=3))
                    
                    fig.add_shape(type="line",
                        x0=levels_2[i - 2][1], y0=levels_2[i - 2][0], x1=df['Date'].iloc[-1], y1=levels_2[i - 2][0],
                        line=dict(color='Green', width=3))

                    charts.append({'fig':fig.to_html(), 'symbol':symbol})

    return charts


def get_chart_deal_zoom(deal):
    symbol = deal[1]
    side = deal[2]
    price_open = deal[4]
    date_open = deal[5]
    price_close = deal[6]
    date_close = deal[7]
    comment = deal[9]
    split_lines = comment.split(';')
    type = int(split_lines[0].split('=')[1])
    price_level_1 = float(split_lines[1].split('=')[1])
    date_level_1 = split_lines[2].split('=')[1]
    price_level_2 = float(split_lines[3].split('=')[1])
    date_level_2 = split_lines[4].split('=')[1]
    price_level_3 = float(split_lines[5].split('=')[1])
    date_level_3 = split_lines[6].split('=')[1]
    

    date_level_1 = datetime.strptime(date_level_1, "%Y-%m-%d %H:%M:%S")
    date_level_2 = datetime.strptime(date_level_2, "%Y-%m-%d %H:%M:%S")
    date_level_3 = datetime.strptime(date_level_3, "%Y-%m-%d %H:%M:%S")

    


    date_from = date_open - timedelta(hours=1)
    date_to = date_close + timedelta(hours=1)
    
    
    df = pd.DataFrame(get_candles_by_symbol_tf(symbol, 5), columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])
    df = df[(df['Date'] > date_from) & (df['Date'] < date_to)]
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.add_scatter(x = [date_open], y = [price_open], mode='markers', marker=dict(size=10, color="Green"))
    fig.add_scatter(x = [date_close], y = [price_close], mode='markers', marker=dict(size=10, color="Red"))

    color = ''

    if type == 1:
        color = 'Red'
    else:
        color = 'Green'
    
    fig.add_shape(type="line",
                        x0=date_from, y0=price_level_1, x1=date_open, y1=price_level_1,
                        line=dict(color=color, width=3))
    
    fig.add_shape(type="line",
                        x0=date_from, y0=price_level_2, x1=date_open, y1=price_level_2,
                        line=dict(color=color, width=3))
    
    fig.add_shape(type="line",
                        x0=date_from, y0=price_level_3, x1=date_open, y1=price_level_3,
                        line=dict(color=color, width=3))

    return fig.to_html()


def get_chart_deal(deal):

    symbol = deal[1]
    side = deal[2]
    price_open = deal[4]
    date_open = deal[5]
    price_close = deal[6]
    date_close = deal[7]
    comment = deal[9]
    split_lines = comment.split(';')
    type = int(split_lines[0].split('=')[1])
    price_level_1 = float(split_lines[1].split('=')[1])
    date_level_1 = split_lines[2].split('=')[1]
    price_level_2 = float(split_lines[3].split('=')[1])
    date_level_2 = split_lines[4].split('=')[1]
    price_level_3 = float(split_lines[5].split('=')[1])
    date_level_3 = split_lines[6].split('=')[1]
    

    date_level_1 = datetime.strptime(date_level_1, "%Y-%m-%d %H:%M:%S")
    date_level_2 = datetime.strptime(date_level_2, "%Y-%m-%d %H:%M:%S")
    date_level_3 = datetime.strptime(date_level_3, "%Y-%m-%d %H:%M:%S")

    


    date_from = date_level_3 - timedelta(hours=1)
    date_to = date_close + timedelta(hours=1)
    
    
    df = pd.DataFrame(get_candles_by_symbol_tf(symbol, 5), columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])
    df = df[(df['Date'] > date_from) & (df['Date'] < date_to)]
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.add_scatter(x = [date_open], y = [price_open], mode='markers', marker=dict(size=10, color="Green"))
    fig.add_scatter(x = [date_close], y = [price_close], mode='markers', marker=dict(size=10, color="Red"))

    color = ''

    if type == 1:
        color = 'Red'
    else:
        color = 'Green'
    
    fig.add_shape(type="line",
                        x0=date_level_1, y0=price_level_1, x1=date_open, y1=price_level_1,
                        line=dict(color=color, width=3))
    
    fig.add_shape(type="line",
                        x0=date_level_2, y0=price_level_2, x1=date_open, y1=price_level_2,
                        line=dict(color=color, width=3))
    
    fig.add_shape(type="line",
                        x0=date_level_3, y0=price_level_3, x1=date_open, y1=price_level_3,
                        line=dict(color=color, width=3))

    return fig.to_html()


def get_chart_level(id):

    level = get_level_by_id(id)
    symbol = level[1]
    price = level[3]
    type = level[4]
    date_start = level[5]

    df = pd.DataFrame(get_candles_by_symbol_tf(symbol, 5), columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
    
    fig.update_layout(xaxis_rangeslider_visible=False)

    color = ''
    if type == 1:
        color = 'Red'
    else:
         color = 'Green'
    fig.add_shape(type="line",
                        x0=date_start, y0=price, x1=df['Date'].iloc[-1], y1=price,
                        line=dict(color=color, width=3))

    return fig.to_html()


def get_chart_with_impulse(df, impulse, tf, symbol):
    #fig = px.line(df, x = 'Date', y = 'Close')

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    add_min = 0
    if tf == 5:
        add_min = 15
    elif tf == 15:
        add_min = 60
    elif tf == 30:
        add_min = 120
    elif tf == 60:
        add_min = 240

    dateEnd = impulse[7] + timedelta(minutes=add_min)
    
    need_type_level = 0
    color = ''
    if impulse[2] == 'L':
        color = 'Green'
        need_type_level = 2
    else:
        color = 'Red'
        need_type_level = 1

    fig.add_shape(type="rect",
                          x0=impulse[5], y0=impulse[4], x1=dateEnd, y1=impulse[6],
                          line=dict(color=color))

    order_book_list_s = get_order_book_by_symbol_s(symbol)
    order_book_list_f = get_order_book_by_symbol_f(symbol)

    up_price = 0
    down_price = 0
    if impulse[2] == 'L':
        up_price = impulse[6]
        up_price += up_price * 0.01

        down_price = impulse[4]
    else:
        up_price = impulse[4]

        down_price = impulse[6]
        down_price -= down_price * 0.01

    for order in order_book_list_s:
        if order[3] < up_price and order[3] > down_price and order[6] == True:
                        fig.add_shape(type="line",
                                       x0=order[7], y0=order[3], x1=df['Date'].iloc[-1], y1=order[3],
                                      line=dict(color='Blue', width=3))
    
    for order in order_book_list_f:
        if order[3] < up_price and order[3] > down_price and order[6] == True:
                        fig.add_shape(type="line",
                                       x0=order[7], y0=order[3], x1=df['Date'].iloc[-1], y1=order[3],
                                      line=dict(color='Red', width=3))

    return fig.to_html()