import psycopg2
from psycopg2 import pool
import io, csv
from datetime import datetime

postgreSQL_pool = pool.ThreadedConnectionPool(1, 100, user="fr3sto",
                                                         password="endorphin25",
                                                         host='db',
                                                         #port=5432,
                                                         database="Screener2")
# # DELETE

# def delete_all_alert_levels():
#     cursor.execute('delete from Alert_Level')
#     conn.commit()


def delete_order_book():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('delete from Order_Book')
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_all_impulses():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('delete from Impulse')
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_all_close_levels():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('delete from Close_Level')
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_all_currency():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('delete from Currency')
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_all_candles():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('delete from Candles')
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_all_levels():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('delete from Levels')
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_level(symbol, date_start):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Levels WHERE Symbol = %s and Date_Start = %s", (symbol,date_start))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_closed_level(symbol, tf, date_start):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Levels WHERE Symbol = %s and TF = %s and Date_Start = %s", (symbol,tf, date_start))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_impulse(symbol, tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Impulse WHERE Symbol = %s and TF = %s", (symbol,tf))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_close_level(symbol, price):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Close_Level WHERE Symbol = %s and Price = '%s'", (symbol,price))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)


def delete_alert_level(symbol, price):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Alert_Level WHERE Symbol = %s and Price = '%s'", (symbol,price))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def delete_position(symbol):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Position WHERE Symbol = %s", (symbol,))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

# # UPDATE

def update_close_level(symbol, date_start, left_pips, price_order_s, pow_s, date_start_s):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute("UPDATE Close_Level SET Left_Pips = %s, Price_Order_S = %s, Pow_S = %s, Date_Start_Order_S = %s WHERE Symbol = %s and Date_Start = %s", (left_pips,price_order_s,pow_s,date_start_s, symbol,date_start))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def update_position(symbol, left_pips_take, left_pips_stop):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute("UPDATE Position SET Left_Pips_Take = %s, Left_Pips_Stop = %s WHERE Symbol = %s", (left_pips_take,left_pips_stop,symbol))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

# def update_alert_level(symbol, date_start, price_order_f, pow_f,left_pips):
#     connection = postgreSQL_pool.getconn()
#     cursor = connection.cursor()
#     cursor.execute("UPDATE Alert_Level SET Left_Pips = %s, Price_Order_F = %s, Pow_F = %s WHERE Symbol = %s and Date_Start = %s", (left_pips, price_order_f, pow_f, symbol,date_start))
#     connection.commit()
#     cursor.close()
#     postgreSQL_pool.putconn(connection)

# # INSERT

def insert_impulse(symbol, type, tf, impulse):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    sql = 'INSERT INTO Impulse(Symbol,TF, Type, Price_Start, Date_Start, Price_End, Date_End, Is_Open) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql, (symbol,tf, type, impulse['price_start'], impulse['date_start'], impulse['price_end'], impulse['date_end'], impulse['is_open']))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def insert_position(symbol,type, price_open,date_open,side, quantity,stop,take,left_pips_take, left_pips_stop):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    sql = 'INSERT INTO Position(Symbol,Type, Price_Open, Date_Open, Side,Quantity, Stop, Take, Left_Pips_Take, Left_Pips_Stop) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql, (symbol,type,price_open,date_open,side,quantity,stop,take,left_pips_take,left_pips_stop))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def insert_close_level(symbol, price, type, left_pips, date_start):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    sql = 'INSERT INTO Close_Level(Symbol, Price, Type, Left_Pips,Date_Start, Price_Order_S, Pow_S, Date_Start_Order_S) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql, (symbol, price,type, left_pips, date_start,0,0, datetime.now()))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def insert_alert_level(symbol, price, type,price_order_f,pow_f, left_pips, date_start):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    sql = 'INSERT INTO Alert_Level(Symbol, Price, Type, Price_Order_F, Pow_F, Price_Order_S, Pow_S, Left_Pips,Date_Start) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql, (symbol, price,type,price_order_f,pow_f,0,0, left_pips, date_start))
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)         

def insert_order_book(order_book):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    f = io.StringIO()
    writer = csv.writer(f)
    for symbol, types in order_book.items():
        for type, prices in types.items():
            for price, order in prices.items():
                writer.writerow([symbol, type, price, order['pow'], order['quantity'], int(order['is_not_mm']), order['date_start'], order['date_end']])
    f.seek(0)
    cursor.copy_expert("COPY Order_Book (Symbol,Type, Price, Pow, Quantity, Is_Not_MM, Date_Start, Date_End) FROM STDIN WITH csv", f)
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def insert_currency(currency_dict):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    f = io.StringIO()
    writer = csv.writer(f)
    for symbol, values in currency_dict.items():
        writer.writerow([symbol, values['min_step']])
    f.seek(0)
    cursor.copy_expert("COPY Currency (Symbol,Min_Step) FROM STDIN WITH csv", f)
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def insert_candles_bulk(candles_dict):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    f = io.StringIO()
    writer = csv.writer(f)
    for symbol, candles in candles_dict.items():
        for candle in candles:
            res_list = candle.copy()
            res_list.insert(0,symbol.split('-')[0])
            res_list.insert(1,symbol.split('-')[1])
            writer.writerow(res_list)
    f.seek(0)
    cursor.copy_expert("COPY Candles (Symbol,TF, Open, High, Low, Close,Volume, Date) FROM STDIN WITH csv", f)
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def insert_levels(level_dict, tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    f = io.StringIO()
    writer = csv.writer(f)
    for symbol, prices in level_dict.copy().items():
        for price, level in prices.items():
            res_list = list(level.copy().values())
            res_list.insert(0, tf)
            res_list.insert(0,symbol)
            writer.writerow(res_list)
    f.seek(0)
    cursor.copy_expert("COPY Levels (Symbol,TF, Price, Type, Date_Start) FROM STDIN WITH csv", f)
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)
# # GET

# def get_all_currency():
#     cursor.execute('SELECT * FROM Currency')
#     currencies = cursor.fetchall()
#     return currencies 

def get_all_impulses():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Impulse')
    impulses = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return impulses

def get_impulses_by_tf(tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Impulse Where TF = %s',(tf,))
    impulses = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return impulses

def get_all_levels():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Levels')
    levels = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return levels

def get_levels_by_tf(tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Levels Where TF = %s',(tf,))
    levels = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return levels

def get_candles_by_symbol(symbol):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Candles where Symbol = %s ORDER by date',(symbol,))
    candles = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return candles

def get_candles_by_tf(tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Candles where TF = %s ORDER by date',(tf,))
    candles = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return candles

def get_candles_by_symbol_tf(symbol, tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Candles where Symbol = %s and TF = %s  ORDER by date',(symbol,tf))
    candles = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return candles

def get_order_book():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Order_Book')
    order_book = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return order_book 

# # CREATE TABLE

def create_table_candles():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE Candles(
            id serial PRIMARY KEY,
            Symbol varchar(20) NOT NULL,
            TF integer NOT NULL,
            Open real NOT NULL,
            High real NOT NULL,
            Low real NOT NULL,
            Close real NOT NULL,
            Volume real NOT NULL,
            Date timestamp without time zone NOT NULL);"""
    )   


    print('Table created successfully')
        
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def create_table_levels():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE Levels(
            id serial PRIMARY KEY,
            Symbol varchar(20) NOT NULL,
            TF integer NOT NULL,
            Price real NOT NULL,
            Type integer NOT NULL,
            Date_Start timestamp without time zone NOT NULL);"""
    )   


    print('Table created successfully')
        
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def create_table_currency():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE Currency(
            id serial PRIMARY KEY,
            Symbol varchar(20) NOT NULL,
            Min_Step real NOT NULL);"""
    )   


    print('Table created successfully')
        
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def create_table_close_level():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE Close_Level(
            id serial PRIMARY KEY,
            Symbol varchar(20) NOT NULL,
            Price real NOT NULL,
            Type integer NOT NULL,
            Left_Pips real NOT NULL,
            Price_Order_S real NOT NULL,
            Pow_S real NOT NULL,
            Date_Start_Order_S timestamp without time zone NOT NULL,
            Date_Start timestamp without time zone NOT NULL);"""
    )  


    print('Table created successfully')
        
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def create_table_positions():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE Position(
            id serial PRIMARY KEY,
            Symbol varchar(20) NOT NULL,
            Type integer NOT NULL,
            Price_Open real NOT NULL,
            Date_Open timestamp without time zone NOT NULL,
            Side varchar(20) NOT NULL,
            Quantity real NOT NULL,
            Stop real NOT NULL,
            Take real NOT NULL,
            Left_Pips_Take integer NOT NULL,
            Left_Pips_Stop integer NOT NULL);"""
    )  


    print('Table created successfully')
        
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def create_table_alert_level():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE Alert_Level(
            id serial PRIMARY KEY,
            Symbol varchar(20) NOT NULL,
            Price real NOT NULL,
            Type integer NOT NULL,
            Price_Order_F real NOT NULL,
            Pow_F real NOT NULL,
            Price_Order_S real NOT NULL,
            Pow_S real NOT NULL,
            Left_Pips real NOT NULL,
            Date_Start timestamp without time zone NOT NULL);"""
    )  


    print('Table created successfully')
        
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def create_table_impulse():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE Impulse(
            id serial PRIMARY KEY,
            Symbol varchar(20) NOT NULL,
            Type varchar(5) NOT NULL,
            TF integer NOT NULL,
            Price_Start real NOT NULL,
            Date_Start timestamp without time zone NOT NULL,
            Price_End real NOT NULL,
            Date_End timestamp without time zone NOT NULL,
            Is_Open integer NOT NULL);"""
    )  


    print('Table created successfully')
        
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

def create_table_order_book():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE Order_Book(
            id serial PRIMARY KEY,
            Symbol varchar(20) NOT NULL,
            Type varchar(10) NOT NULL,
            Price real NOT NULL,
            Pow real NOT NULL,
            Quantity real NOT NULL,
            Is_Not_MM int NOT NULL,
            Date_Start timestamp without time zone NOT NULL,
            Date_End timestamp without time zone NOT NULL);"""
    )  


    print('Table created successfully')
        
    connection.commit()
    cursor.close()
    postgreSQL_pool.putconn(connection)

if __name__ == '__main__':
    pass
    #create_table_impulse()
    #create_table_positions()
    #create_table_alert_level()
    #create_table_close_level()
    #create_table_candles()
    #create_table_levels()
    #create_table_currency()
    #create_table_order_book()