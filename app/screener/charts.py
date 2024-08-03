import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime
from plotly.subplots import make_subplots

def chart_with_flat(df_candles, flat):#, order_book):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Candlestick(x=df_candles['Date'],
                                         open=df_candles['Open'], high=df_candles['High'],
                                         low=df_candles['Low'], close=df_candles['Close'],  increasing_line_color= 'gray', decreasing_line_color= 'gray'), secondary_y=True)

    fig.update_layout(xaxis_rangeslider_visible=False, template = 'plotly_dark')

    side_flat = flat[3]
    up_flat = flat[4]
    down_flat = flat[5]
    date_start = flat[6]
    date_end = flat[7]
    up_range = flat[8]
    down_range = flat[9]
    now = datetime.now()

    if side_flat == -1:
        fig.add_trace(go.Scatter(x=[date_start, date_start,
                                date_end,date_end,
                                date_start],
                                    y=[up_flat, down_flat, down_flat, up_flat, up_flat],
                                    line=dict(color='rgba(255,255,0, 0.3)'),fillcolor='rgba(255,255,0, 0.1)', fill="toself", mode='lines'), secondary_y=True)
    else:
        fig.add_trace(go.Scatter(x=[date_start, date_start,
                                date_end,date_end,
                                date_start],
                                    y=[up_flat, down_flat, down_flat, up_flat, up_flat],
                                    line=dict(color='rgba(255,255,0, 0.3)'),fillcolor='rgba(255,255,0, 0.1)', fill="toself", mode='lines'), secondary_y=True)

    fig.add_trace(go.Scatter(x=[date_end, date_end,
                                now,now,
                                date_end],
                                    y=[up_range, down_range, down_range, up_range, up_range],
                                    line=dict(color='rgba(139,0,255, 0.3)'), fillcolor='rgba(139,0,255, 0.2)', fill="toself", mode='lines'), secondary_y=True)

    # max_price = max(df_candles['High'])
    # start_date_candles = df_candles['Date'].iloc[0]
    # min_price = min(df_candles['Low'])

    # x_line_bids = []
    # y_line_bids = []

    # x_line_asks = []
    # y_line_asks = []

    # for ob in order_book:
    #     type = ob[2]
    #     price = ob[3]
    #     date_start = ob[7]
    #     date_end = ob[8]

    #     if price < max_price and price > min_price:
    #         if date_start > start_date_candles:
    #             if price < df_candles['Close'].iloc[-1]:
    #                 x_line_bids.extend([date_start, df_candles['Date'].iloc[-1], None])
    #                 y_line_bids.extend([price, price,None])
    #             else:
    #                 x_line_asks.extend([date_start, df_candles['Date'].iloc[-1], None])
    #                 y_line_asks.extend([price, price,None])


    # fig.add_trace(go.Scatter(x = x_line_bids, y=y_line_bids, mode='lines', line=dict(color='Green', width=3)), secondary_y=True)
    # fig.add_trace(go.Scatter(x = x_line_asks, y=y_line_asks, mode='lines', line=dict(color='Red', width=3)), secondary_y=True)

    fig.add_trace(go.Bar(x=df_candles['Date'], y=df_candles['Volume']),
               secondary_y=False)
    
    fig.update_layout(yaxis=dict(range=[0, 4*df_candles['Volume'].max()]))

    return fig.to_html()


def get_chart_with_impulse(df, impulse,levels,orders, tf, symbol):
    #fig = px.line(df, x = 'Date', y = 'Close')

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
    
    fig.update_layout(xaxis_rangeslider_visible=False,  template = 'plotly_dark')
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
    
    for level in levels:
        price = level[3]
        type = level[4]
        date_start = level[5]

        color = ''
        if type == 1:
            color = 'Red'
        else:
            color = 'Green'
        fig.add_shape(type="line",
                            x0=date_start, y0=price, x1=df['Date'].iloc[-1], y1=price,
                            line=dict(color=color, width=3))
        

    for order in orders:
        price = order[3]
        type = order[2]
        date_start = order[7]
        is_not_mm = order[6]

        color = 'Red' if type == 'asks' else 'Green'
        if order[1] == symbol and order[3] < up_price and order[3] > down_price:
            if (order[8] - order[7]).total_seconds() / 60 > 30:
                fig.add_shape(type="line",
                                x0=date_start, y0=price, x1=df['Date'].iloc[-1], y1=price,
                                line=dict(color=color, width=3, dash="dash"))

    return fig.to_html()