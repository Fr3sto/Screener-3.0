import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime
import plotly.express as px

from screener.database import (get_candles_by_symbol, 
                               get_candles_by_symbol_tf, get_level_by_id,
                               get_all_levels, get_position_by_symbol)

from screener.exchange import get_candles_by_date


def get_chart_current_position(pos):


    exchange = pos[1]
    type_exchange = pos[2]
    symbol = pos[3]
    side = pos[4]
    quantity = pos[5]
    price_open = pos[6]
    date_open = pos[7]
    stop = pos[8]
    take = pos[11]
    comment = pos[14]
    split_lines = comment.split(';')
    type = split_lines[3].split('=')[1]
    price_order = float(split_lines[4].split('=')[1])
    date_start_order = split_lines[7].split('=')[1]

    

    date_start_order = datetime.strptime(date_start_order, "%Y-%m-%d %H:%M:%S.%f")

    date_from = date_start_order - timedelta(hours=2)
    date_to = datetime.now()
    
    
    df = get_candles_by_date(exchange, type_exchange, symbol, date_from, date_to)
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.add_scatter(x = [date_open], y = [price_open], mode='markers', marker=dict(size=10, color="Green"))

    
    fig.add_shape(type="line",
                        x0=date_start_order, y0=price_order, x1=date_to, y1=price_order,
                        line=dict(color='Red', width=3))
    
    fig.add_shape(type="line",
                        x0=date_open, y0=take, x1=date_to, y1=take,
                        line=dict(color='Green', width=3))

    return fig.to_html()



def get_chart_equity(deals):
    
    profits = []
    sum_percent = 0
    i = 1
    for deal in reversed(deals):
        profit = deal[10]
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
    exchange = deal[1]
    type_exchange = deal[2]
    symbol = deal[3]
    side = deal[4]
    price_open = deal[6]
    date_open = deal[7]
    price_close = deal[8]
    date_close = deal[9]
    comment = deal[11]
    split_lines = comment.split(';')
    type = split_lines[3].split('=')[1]
    price_order = float(split_lines[4].split('=')[1])
    date_start_order = split_lines[7].split('=')[1]

    

    date_start_order = datetime.strptime(date_start_order, "%Y-%m-%d %H:%M:%S.%f")


    

    date_from = date_start_order
    date_to = date_close + timedelta(hours=2)
    
    
    df = get_candles_by_date(exchange, type_exchange, symbol, date_from, date_to)

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


def get_chart_deal_rebound_level(deal):

    exchange = deal[1]
    type_exchange = deal[2]
    symbol = deal[3]
    side = deal[4]
    price_open = deal[6]
    date_open = deal[7]
    price_close = deal[8]
    date_close = deal[9]
    comment = deal[11]
    split_lines = comment.split(';')
    type = split_lines[3].split('=')[1]
    price_order = float(split_lines[4].split('=')[1])
    date_start_order = split_lines[7].split('=')[1]

    

    date_start_order = datetime.strptime(date_start_order, "%Y-%m-%d %H:%M:%S.%f")


    

    date_from = date_start_order - timedelta(hours=20)
    date_to = date_close + timedelta(hours=8)
    
    
    df = get_candles_by_date(exchange, type_exchange, symbol, date_from, date_to)

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