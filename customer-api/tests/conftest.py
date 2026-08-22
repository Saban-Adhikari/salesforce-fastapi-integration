import sqlite3
import pytest
import customer_service

@pytest.fixture
def test_database(tmp_path, monkeypatch):
    database = tmp_path / "test_customers.db"

    connection = sqlite3.connect(database)

    connection.execute(
        """
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
        """
    )


    def test_get_connection():
        connection = sqlite3.connect(database)
        connection.row_factory = sqlite3.Row
        return connection

    monkeypatch.setattr(
        customer_service,
        "get_connection",
        test_get_connection
    )

    connection.commit()
    connection.close()

    return database

@pytest.fixture
def example_customer():
    return {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "555-0000"
    }