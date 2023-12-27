import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime

from screener.database import get_candles_by_symbol, get_order_book_by_symbol, get_candles_by_symbol_tf

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



def get_chart_deal(deal):

    symbol = deal[1]
    side = deal[2]
    price_open = deal[4]
    date_open = deal[5]
    price_close = deal[6]
    date_close = deal[7]
    comment = deal[9]
    split_lines = comment.split(';')
    stop = split_lines[0]
    time_live = float(split_lines[1])
    type = split_lines[2]
    price_start = split_lines[3]
    date_start = split_lines[4]
    price_end = split_lines[5]
    date_end = split_lines[6]
    tf = int(split_lines[7])
    

    date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

    


    date_from = date_start - timedelta(hours=3)
    date_to = date_close + timedelta(hours=3)
    
    
    df = pd.DataFrame(get_candles_by_symbol_tf(symbol, tf), columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    df = df.sort_values(by=['Date'])
    df = df[(df['Date'] > date_from) & (df['Date'] < date_to)]
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.add_scatter(x = [date_open], y = [price_open], mode='markers', marker=dict(size=10, color="Green"))
    fig.add_scatter(x = [date_close], y = [price_close], mode='markers', marker=dict(size=10, color="Red"))


    
    color = 'Red'
    if type == 'L':
         color = 'Green'
    fig.add_shape(type="rect",
                          x0=date_start, y0=price_start, x1=date_end, y1=price_end,
                          line=dict(color=color))
    

    date_from_order = date_open - timedelta(minutes=time_live)
    fig.add_shape(type="line",
                        x0=date_from_order, y0=stop, x1=date_open, y1=stop,
                        line=dict(color='Blue', width=3))

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