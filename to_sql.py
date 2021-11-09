# We are going to push registers to a postgres sql database

# This is a test file for the sql connection
# Later on, we are going to make the final changes to fastfood script

from pymongo import MongoClient
import pymongo

import psycopg2

# CREATE TABLE rha_dish(id SERIAL PRIMARY KEY NOT NULL, dish CHAR(20) NOT NULL, price FLOAT NOT NULL);
# CREATE TABLE rha_ingredients(id SERIAL PRIMARY KEY NOT NULL, ingredient CHAR(20) NOT NULL, price FLOAT NOT NULL);
# INSERT INTO rha_dish( dish, price ) VALUES ();

# CREATE TABLE rha_orders(id SERIAL PRIMARY KEY NOT NULL, order_id CHAR(30) NOT NULL, date DATE NOT NULL, dish CHAR(50) NOT NULL, price_uni FLOAT NOT NULL, qty FLOAT NOT NULL, price_t FLOAT NOT NULL);

# CREATE TALBE rha_users(id SERIAL PRIMARY KEY NOT NULL, name CHAR(30) NOT NULL, age INT, )

def postgress():
    conexion = psycopg2.connect( "dbname=ramon_hinojosa_d user=ramon_hinojosa password=ramon_hinojosa123*" )

    cur = conexion.cursor()
    cur.execute( "select * from rha;" )
    cur.execute(
        "INSERT INTO rha ( comida, qty, price_uni, price_t ) VALUES ( 'hamburguesa', 1, 100, 100 );"
    )
    conexion.commit()

    cur.close()
    conexion.close()

    print("Postgress Success!")

def mongo():


    print("Mongo Success!")

if __name__ == "__main__":
    postgress()
    # mongo()

