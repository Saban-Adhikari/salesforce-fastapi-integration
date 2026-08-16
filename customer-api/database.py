# import sqlite3

# connection = sqlite3.connect("customers.db")

# cursor = connection.cursor()

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS customers (
#          id INTEGER PRIMARY KEY AUTOINCREMENT,
#          name TEXT NOT NULL
#          )
#     """)

# cursor.execute("INSERT INTO customers (name) VALUES (?)", ("John Smith",))
# cursor.execute("INSERT INTO customers (name) VALUES (?)", ("Sarah Jones",))
# cursor.execute("INSERT INTO customers (name) VALUES (?)", ("Bob Williams",))

# connection.commit()
# connection.close()

import sqlite3


def get_connection():
    connection = sqlite3.connect("customers.db")
    connection.row_factory = sqlite3.Row
    return connection