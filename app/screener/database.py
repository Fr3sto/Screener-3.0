from psycopg2 import pool
from sshtunnel import SSHTunnelForwarder

server =  SSHTunnelForwarder(
    ('31.129.99.176', 22), #Remote server IP and SSH port
    ssh_username = "root",
    ssh_password = "Endorphin25)",
    remote_bind_address=('localhost', 1234),
    local_bind_address=('localhost', 1234)) #PostgreSQL server IP and sever port on remote machine
        
server.start()   

postgreSQL_pool = pool.ThreadedConnectionPool(1, 100, user="fr3sto",
                                                         password="endorphin25",
                                                         host=server.local_bind_host,
                                                         port=server.local_bind_port,
                                                         database="Screener")

# postgreSQL_pool = pool.ThreadedConnectionPool(1, 100, user="fr3sto",
#                                                          password="endorphin25",
#                                                          host='10.16.0.2',
#                                                          port=1234,
#                                                          database="Screener")

# GET

def get_all_currency():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM All_Currency')
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    postgreSQL_pool.putconn(connection)

    symbols_ob = dict()

    for curr in result:
        exchange = curr[1]
        type = curr[2]
        symbol = curr[3]
        min_step = curr[4]
        
        if not exchange in symbols_ob:
            symbols_ob[exchange] = dict()
        
        if not type in symbols_ob[exchange]:
            symbols_ob[exchange][type] = dict()

        symbols_ob[exchange][type][symbol] = {'min_step':float(min_step)}

        
    return symbols_ob

def get_all_impulses():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Impulse')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_status():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * from Status_Service')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_candles_by_symbol_tf(symbol,tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Candles where Symbol = %s and TF = %s',(symbol,tf))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_impulse_opened(symbol, tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Impulse Where Symbol = %s and TF = %s', (symbol, tf))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_all_order_book():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM All_Order_Book')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_order_book_by_symbol(symbol):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM All_Order_Book WHERE Symbol = %s',(symbol,))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_all_levels():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Levels')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_levels_by_symbol_tf(symbol, tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Levels Where Symbol = %s and TF = %s', (symbol, tf))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result