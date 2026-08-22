import sqlite3

TEST_DATABASE = 'test_cusomers.db'

def get_test_connection():
    connection = sqlite3.connect(TEST_DATABASE)

    connection.row_factory = sqlite3.Row
    return connection