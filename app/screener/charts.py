import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime
import plotly.express as px

def chart_with_cubes(df_candles, df_price_amount):
    fig = go.Figure(data=[go.Candlestick(x=df_candles['Date'],
                                         open=df_candles['Open'], high=df_candles['High'],
                                         low=df_candles['Low'], close=df_candles['Close'],  increasing_line_color= 'gray', decreasing_line_color= 'gray')])

    fig.update_layout(xaxis_rangeslider_visible=False, template = 'plotly_dark')

    fig.add_scatter(x = df_price_amount['Date'], y = df_price_amount['Price'], mode='markers', marker=dict(size=15,symbol = 'square-open', color='Yellow'))

    return fig.to_html()