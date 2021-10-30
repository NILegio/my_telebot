import sqlite3
from sqlite3 import Error

def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close()

def create_db():
    db = "goods.db"
    sql_create_goods_table = """CREATE TABLE IF NOT EXISTS goods(vendor_code INT PRIMARY KEY,
                              brand TEXT DEFAULT "",
                              title TEXT DEFAULT "");"""
    conn = create_connection(db)
    if conn is not None:
        create_table(conn, sql_create_goods_table)
    else: print ("Error! Cannot create database connection")



def create_goods(vendor_code, data, type):
    sql_insert = """INSERT INTO goods(vendor_code, {0}) VALUES(?, ?)"""
    sql_update = """UPDATE goods SET vendor_code=?, {0}=? WHERE vendor_code={1}"""
    sql_select = """SELECT vendor_code FROM goods WHERE vendor_code={0}"""
    db = "goods.db"
    conn = create_connection(db)
    cur = conn.cursor()
    check = cur.execute(sql_select.format(vendor_code))
    if check.fetchall():
        cur.execute(sql_update.format(type, vendor_code), (vendor_code, data))
    else:
        cur.execute(sql_insert.format(type), (vendor_code, data))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()