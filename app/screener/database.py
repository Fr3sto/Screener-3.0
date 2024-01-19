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
    cursor.execute('SELECT * FROM Currency')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)

    currency_dict = dict()

    for curr in result:
        currency_dict[curr[1]] = {'min_step':curr[2], 'min_qty':curr[3], 'price_scale':curr[4]}
    return currency_dict

def get_position_by_symbol(symbol):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Position where Symbol = %s',(symbol,))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_deal_by_id(id):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Deals where id = %s',(id,))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_all_order_book_f():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * from order_book_f where extract(epoch from date_end - date_start) / 60 > 5')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_all_status_check():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Status_Service')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result


def get_all_positions():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Position')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_all_deals():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Deals order by Date_Close desc')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

        

def get_candles_by_symbol(symbol):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Candles where Symbol = %s',(symbol,))
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


def get_all_levels():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * from Levels')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_level_by_id(id):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * from Levels where id = %s',(id,))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_close_levels():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * from Close_Level')    
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

