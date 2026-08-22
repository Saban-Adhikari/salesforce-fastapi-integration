import sqlite3


DATABASE = "customers.db"


def get_connection(database=DATABASE):
    connection = sqlite3.connect(database)

    connection.row_factory = sqlite3.Row

    return connection