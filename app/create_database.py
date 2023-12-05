import psycopg2
from psycopg2 import pool
import io, csv
from datetime import datetime

postgreSQL_pool = pool.ThreadedConnectionPool(1, 100, user="fr3sto",
                                                         password="endorphin25",
                                                         database="Screener",
                                                         host='db',
                                                         port=5432)

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
        """ CREATE TABLE Order_Book_S(
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
    create_table_impulse()
    create_table_positions()
    create_table_close_level()
    create_table_candles()
    create_table_levels()
    create_table_currency()
    create_table_order_book()