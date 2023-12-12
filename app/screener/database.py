import psycopg2

conn = psycopg2.connect(database='Screener', user='fr3sto', password='endorphin25',host='10.16.0.2', port=1234)
curs = conn.cursor()

# GET

def get_all_currency():
    curs.execute('SELECT * FROM Currency order by Symbol')
    currencies = curs.fetchall()
    return currencies 

def get_all_positions():
    curs.execute('SELECT * FROM Position')
    positions = curs.fetchall()
    return positions 

def get_all_impulses():
    curs.execute('SELECT * FROM Impulse')
    positions = curs.fetchall()
    return positions 

        
def get_impulse_opened(symbol, tf):
    curs.execute('SELECT * FROM Impulse Where Symbol = %s and TF = %s', (symbol, tf))
    impulse = curs.fetchall()
    return impulse
    

def get_candles_by_symbol(symbol):
    curs.execute('SELECT * FROM Candles where Symbol = %s',(symbol,))
    candles = curs.fetchall()
    return candles

def get_candles_by_symbol_tf(symbol,tf):
    curs.execute('SELECT * FROM Candles where Symbol = %s and TF = %s',(symbol,tf))
    candles = curs.fetchall()
    return candles


def get_all_order_book():
    curs.execute('SELECT * from order_book where extract(epoch from date_end - date_start) / 60 > 15')
    levels = curs.fetchall()
    return levels

def get_order_book_by_symbol(symbol):
    curs.execute('SELECT * from order_book where extract(epoch from date_end - date_start) / 60 > 15 and Symbol = %s',(symbol,))
    levels = curs.fetchall()
    return levels

