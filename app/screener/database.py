from psycopg2 import pool
# from sshtunnel import SSHTunnelForwarder

# server =  SSHTunnelForwarder(
#     ('31.129.99.176', 22), #Remote server IP and SSH port
#     ssh_username = "root",
#     ssh_password = "Endorphin25)",
#     remote_bind_address=('localhost', 1234),
#     local_bind_address=('localhost', 1234)) #PostgreSQL server IP and sever port on remote machine
        
# server.start()   

# postgreSQL_pool = pool.ThreadedConnectionPool(1, 100, user="fr3sto",
#                                                          password="endorphin25",
#                                                          host=server.local_bind_host,
#                                                          port=server.local_bind_port,
#                                                          database="Screener")

postgreSQL_pool = pool.ThreadedConnectionPool(1, 100, user="fr3sto",
                                                         password="endorphin25",
                                                         host='10.16.0.2',
                                                         port=1234,
                                                         database="Screener")

# GET

def get_all_currency():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM All_Currency')
    result = cursor.fetchall()
    res_currency = dict()

    for res in result:
        res_currency[res[1]] = {'min_step':res[2], 'min_qty':res[3]}
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return res_currency

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
    cursor.execute('SELECT * FROM Order_Book')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_order_book_by_symbol(symbol):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Order_Book WHERE Symbol = %s',(symbol,))
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