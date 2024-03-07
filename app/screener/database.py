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

def get_currency():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM currency')
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    postgreSQL_pool.putconn(connection)

    symbols_ob = dict()

    for curr in result:
        symbol = curr[1]
        min_step = curr[2]
        
        symbols_ob[symbol] = {'min_step':float(min_step)}

        
    return symbols_ob


def get_order_book():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * from Order_Book where extract(epoch from date_end - date_start) / 60 >= 60')
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