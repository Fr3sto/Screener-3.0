import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime
import plotly.express as px

from screener.database import (get_candles_by_symbol, 
                               get_candles_by_symbol_tf, get_level_by_id,
                               get_all_levels)


def get_chart_close_level(levels_symbol, level_price):
    
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
                if levels_1[i][0] == level_price:
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
                if levels_2[i][0] == level_price:
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

def get_chart_equity(deals):
    
    profits = []
    sum_percent = 0
    i = 1
    for deal in reversed(deals):
        profit = deal[8]
        percent = round(profit / 5 * 100,2)
        sum_percent += percent
        profits.append((sum_percent, i))
        i+=1
    

    colors=['red' if val[0] < 0 else 'green' for val in profits]
    trace = go.Scatter(
        x=[x[1] for x in profits], 
        y=[x[0] for x in profits], 
        mode='markers+lines', 
        marker={'color': colors}, 
        line={'color': 'gray'}
    )

    # crate figure, plot 
    fig = go.Figure(data=trace)
    # df = pd.DataFrame(profits, columns=['profit','id'])
    # fig = px.line(df, x="id", y="profit", title='Equity of deals')
    return fig.to_html()

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
    price_level_3 = 0
    date_level_3 = 0
    if len(split_lines) > 5:
        price_level_3 = float(split_lines[5].split('=')[1])
        date_level_3 = split_lines[6].split('=')[1]
    
    

    date_level_1 = datetime.strptime(date_level_1, "%Y-%m-%d %H:%M:%S")
    date_level_2 = datetime.strptime(date_level_2, "%Y-%m-%d %H:%M:%S")
    if len(split_lines) > 5:
        date_level_3 = datetime.strptime(date_level_3, "%Y-%m-%d %H:%M:%S")

    


    date_from = date_open - timedelta(hours=1)
    date_to = date_close + timedelta(hours=8)
    
    
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
    if len(split_lines) > 5:
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
    price_level_3 = 0
    date_level_3 = 0
    if len(split_lines) > 5:
        price_level_3 = float(split_lines[5].split('=')[1])
        date_level_3 = split_lines[6].split('=')[1]
    

    date_level_1 = datetime.strptime(date_level_1, "%Y-%m-%d %H:%M:%S")
    date_level_2 = datetime.strptime(date_level_2, "%Y-%m-%d %H:%M:%S")
    if len(split_lines) > 5:
        date_level_3 = datetime.strptime(date_level_3, "%Y-%m-%d %H:%M:%S")

    

    date_from = 0
    if type == 1:
        if len(split_lines) > 5:
            date_from = date_level_3 - timedelta(hours=1)
        else:
            date_from = date_level_2 - timedelta(hours=1)
    else:
        date_from = date_level_1 - timedelta(hours=1)
    date_to = date_close + timedelta(hours=8)
    
    
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
    
    if len(split_lines) > 5:
        fig.add_shape(type="line",
                            x0=date_level_3, y0=price_level_3, x1=date_open, y1=price_level_3,
                            line=dict(color=color, width=3))

    return fig.to_html()



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