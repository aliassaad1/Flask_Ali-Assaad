import sqlite3



def get_db_connection():
  
    conn = sqlite3.connect('Users.db')
  
    conn.row_factory= sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
                 
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        country TEXT NOT NULL
    );
    ''')
    conn.commit()
    conn.close()
    