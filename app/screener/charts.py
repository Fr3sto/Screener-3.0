import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime
import plotly.express as px

from screener.database import (get_candles_by_symbol, 
                               get_candles_by_symbol_tf, get_level_by_id,
                               get_all_levels, get_position_by_symbol)


def get_chart_three_close_level(levels_symbol, level_price):
    
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


def get_chart_current_position(symbol):

    position = get_position_by_symbol(symbol)

    price_open = position[0][4]
    date_open = position[0][5]

    stop = position[0][6]
    tp = position[0][8]

    comment = position[0][11]
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


    date_from = date_level_2 - timedelta(hours=1)
    
    
    df = pd.DataFrame(get_candles_by_symbol_tf(symbol, 5), columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])
    df = df[(df['Date'] > date_from)]
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.add_scatter(x = [date_open], y = [price_open], mode='markers', marker=dict(size=10, color="Green"))

    #stop
    fig.add_shape(type="line",
                        x0=date_open, y0=stop, x1=df['Date'].iloc[-1], y1=stop,
                        line=dict(color='Red', width=1))
    
    fig.add_shape(type="line",
                        x0=date_open, y0=tp, x1=df['Date'].iloc[-1], y1=tp,
                        line=dict(color='Green', width=1))


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
                            x0=date_from, y0=price_level_3, x1=date_open, y1=price_level_3,
                            line=dict(color=color, width=3))

    return fig.to_html()



def get_chart_two_close_level(levels_symbol, level_price):
    
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

        if len(levels_1) > 1:
            for i in range(1, len(levels_1)):
                if levels_1[i][0] == level_price:
                    left_1 = abs(100 - levels_1[i][0] / levels_1[i - 1][0] * 100)
                    if left_1 < 0.3:
                        print(f"{symbol} Close levels Up {levels_1[i][0]} {levels_1[i - 1][0]}")
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
            

                        return fig.to_html()


            
        levels_2 = sorted(type[2], key=lambda x: x[0], reverse=True)

        if len(levels_2) > 1:
            for i in range(1, len(levels_2)):
                if levels_2[i][0] == level_price:
                    left_1 = abs(100 - levels_2[i][0] / levels_2[i - 1][0] * 100)
                    if left_1 < 0.3:
                        print(f"{symbol} Close levels Down {levels_2[i][0]} {levels_2[i - 1][0]}")
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
        profit = deal[9]
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


def get_chart_deal_rebound_level_zoom(deal):
    symbol = deal[1]
    side = deal[3]
    price_open = deal[5]
    date_open = deal[6]
    price_close = deal[7]
    date_close = deal[8]
    comment = deal[10]
    split_lines = comment.split(';')
    type = split_lines[0].split('=')[1]
    price_order = float(split_lines[1])
    date_start_order = split_lines[4]

    

    date_start_order = datetime.strptime(date_start_order, "%Y-%m-%d %H:%M:%S.%f")

    date_from = date_open - timedelta(hours=2)
    date_to = date_close + timedelta(hours=2)
    
    
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

    if type == 'asks':
        color = 'Red'
    else:
        color = 'Green'
    
    fig.add_shape(type="line",
                        x0=date_from, y0=price_order, x1=date_open, y1=price_order,
                        line=dict(color=color, width=3))

    return fig.to_html()


def get_chart_deal_rebound_level(deal):

    symbol = deal[1]
    side = deal[3]
    price_open = deal[5]
    date_open = deal[6]
    price_close = deal[7]
    date_close = deal[8]
    comment = deal[10]
    split_lines = comment.split(';')
    type = split_lines[0].split('=')[1]
    price_order = float(split_lines[1])
    date_start_order = split_lines[4]

    

    date_start_order = datetime.strptime(date_start_order, "%Y-%m-%d %H:%M:%S.%f")


    

    date_from = date_start_order - timedelta(hours=20)
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

    if type == 'asks':
        color = 'Red'
    else:
        color = 'Green'
    
    fig.add_shape(type="line",
                        x0=date_start_order, y0=price_order, x1=date_open, y1=price_order,
                        line=dict(color=color, width=3))

    return fig.to_html()

def get_chart_deal_break_level_zoom(deal):
    symbol = deal[1]
    side = deal[3]
    price_open = deal[5]
    date_open = deal[6]
    price_close = deal[7]
    date_close = deal[8]
    comment = deal[10]
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


def get_chart_deal_break_level(deal):

    symbol = deal[1]
    side = deal[3]
    price_open = deal[5]
    date_open = deal[6]
    price_close = deal[7]
    date_close = deal[8]
    comment = deal[10]
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
            date_from = date_level_3 - timedelta(hours=20)
        else:
            date_from = date_level_2 - timedelta(hours=20)
    else:
        date_from = date_level_1 - timedelta(hours=20)
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