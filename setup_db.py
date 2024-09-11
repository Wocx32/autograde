import sqlite3
from sqlite3 import Error

DB_PATH = 'db/db.sqlite'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)

    except Error as e:
        print(e)
    
    if conn:
        return conn

def close_connection(conn):
    # Close the connection
    try:
        conn.close()
    except Error as e:
        print(e)


def setup():
    conn = sqlite3.connect(DB_PATH)

    curse = conn.cursor()

    curse.execute("""
        CREATE TABLE IF NOT EXISTS result (
            id integer PRIMARY KEY AUTOINCREMENT,
            roll_no integer NOT NULL,
            assignment text NOT NULL,
            passed integer NOT NULL,
            failed integer NOT NULL
        );
    """)

if __name__ == '__main__':
    setup()