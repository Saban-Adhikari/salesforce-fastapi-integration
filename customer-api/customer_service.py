from database import get_connection
from models import Customer

def get_all_customers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, email, phone FROM customers"
    )

    customers = cursor.fetchall()

    connection.close()

    return [dict(customer) for customer in customers]


def get_customer_by_id(customer_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, email, phone
        FROM customers
        WHERE id = ?
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    connection.close()

    return customer

def create_customer(customer: Customer):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO customers (name, email, phone)
        VALUES (?, ?, ?)
        """,
        (customer.name, customer.email, customer.phone)
    )

    connection.commit()

    customer_id = cursor.lastrowid

    connection.close()

    return {
        "id": customer_id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone
    }

def update_customer(customer_id: int, customer: Customer):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM customers WHERE id = ?",
        (customer_id,)
    )

    existing_customer = cursor.fetchone()

    if existing_customer is None:
        connection.close()
        return None

    cursor.execute(
        """
        UPDATE customers
        SET name = ?, email = ?, phone = ?
        WHERE id = ?
        """,
        (
            customer.name,
            customer.email,
            customer.phone,
            customer_id
        )
    )

    connection.commit()

    connection.close()

    return {
        "id": customer_id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone
    }

def delete_customer(customer_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM customers WHERE id = ?",
        (customer_id,)
    )

    existing_customer = cursor.fetchone()

    if existing_customer is None:
        connection.close()
        return False

    cursor.execute(
        "DELETE FROM customers WHERE id = ?",
        (customer_id,)
    )

    connection.commit()

    connection.close()

    return True