import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta

from screener.database import get_candles_by_symbol, get_order_book_by_symbol

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

    order_book_list = get_order_book_by_symbol(symbol)

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

    for order in order_book_list:
        if order[3] < up_price and order[3] > down_price and order[6] == True:
                        fig.add_shape(type="line",
                                       x0=order[7], y0=order[3], x1=df['Date'].iloc[-1], y1=order[3],
                                      line=dict(color='Blue', width=3))

    return fig.to_html()