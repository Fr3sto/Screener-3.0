import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime
from plotly.subplots import make_subplots

def chart_with_flat(df_candles, flat):
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


    fig.add_trace(go.Bar(x=df_candles['Date'], y=df_candles['Volume']),
               secondary_y=False)
    
    fig.update_layout(yaxis=dict(range=[0, 4*df_candles['Volume'].max()]))

    return fig.to_html()