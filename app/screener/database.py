import psycopg2
import io, csv
from datetime import datetime


conn = psycopg2.connect(database='Screener', user='fr3sto', password='endorphin25',host='db', port=5432)
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

def get_all_levels():
    curs.execute('SELECT * FROM Levels')
    levels = curs.fetchall()
    return levels

def get_levels_by_symbol_tf(symbol, tf):
    curs.execute('SELECT * FROM Levels Where Symbol = %s and TF = %s', (symbol, tf))
    level = curs.fetchall()
    return level
        
def get_impulse_opened(symbol, tf):
    curs.execute('SELECT * FROM Impulse Where Symbol = %s and TF = %s', (symbol, tf))
    impulse = curs.fetchall()
    return impulse
    
def get_levels_by_symbol(symbol):
    curs.execute('SELECT * FROM Levels where Symbol = %s',(symbol,))
    levels = curs.fetchall()
    return levels

def get_candles_by_symbol(symbol):
    curs.execute('SELECT * FROM Candles where Symbol = %s',(symbol,))
    candles = curs.fetchall()
    return candles

def get_candles_by_symbol_tf(symbol,tf):
    curs.execute('SELECT * FROM Candles where Symbol = %s and TF = %s',(symbol,tf))
    candles = curs.fetchall()
    return candles

def get_all_close_levels():
    curs.execute('SELECT * FROM Close_Level ORDER BY Left_Pips')
    levels = curs.fetchall()
    return levels 

def get_all_alert_levels():
    curs.execute('SELECT * FROM Alert_Level ORDER BY id')
    levels = curs.fetchall()
    return levels 

