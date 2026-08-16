from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection

app = FastAPI()

customers = [
    {
        "id": 1,
        "name": "John Smith"
    },
    {
        "id": 2,
        "name": "Sarah Jones"
    },
    {
        "id": 3,
        "name": "Bob Williams"
    }
]

class Customer(BaseModel):
    name: str
    email: str
    phone: str

@app.delete("/customers/{customer_id}")
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
        raise HTTPException(status_code=404, detail="Customer not found")

    cursor.execute(
        "DELETE FROM customers WHERE id = ?",
        (customer_id,)
    )

    connection.commit()

    connection.close()

    return {
        "message": "Customer deleted"
    }

@app.patch("/customers/{customer_id}")
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
        raise HTTPException(status_code=404, detail="Customer not found")

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

@app.post("/customers")
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

@app.get("/customers")
def get_customers():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT id, name, email, phone FROM customers")

    customers = cursor.fetchall()

    connection.close()

    return[dict(customer) for customer in customers]

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name from customers where id = ?",
        (customer_id,)
    )

    customer = cursor.fetchone()

    connection.close()

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return dict(customer)