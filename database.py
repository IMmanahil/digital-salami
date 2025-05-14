import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# WARNING: This will delete existing users table!
cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        verified INTEGER,
        verification_code TEXT
    )
''')

conn.commit()
conn.close()

print(" Table recreated successfully with correct columns.")
import sqlite3

import sqlite3

def recreate_salami_table():
    conn = sqlite3.connect("salami.db")
    c = conn.cursor()
    
    # WARNING: This will drop the existing table!
    c.execute("DROP TABLE IF EXISTS salami_records")

    c.execute('''
        CREATE TABLE salami_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT,
            sender_email TEXT,              
            sender_account_type TEXT,
            sender_account_number TEXT,
            receiver_name TEXT,
            receiver_email TEXT,              -- Added receiver_email
            receiver_account_type TEXT,
            receiver_account_number TEXT,
            salami_amount TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

    print("salami_records table recreated successfully.")

# Call this function to recreate the table
recreate_salami_table()
