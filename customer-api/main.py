from fastapi import FastAPI, HTTPException
from models import Customer
from customer_service import (
    get_all_customers, 
    get_customer_by_id, 
    create_customer,
    update_customer,
    delete_customer
)

app = FastAPI()

@app.delete("/customers/{customer_id}")
def delete_customer_endpoint(customer_id: int):
    deleted = delete_customer(customer_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "message": "Customer deleted"
    }

@app.patch("/customers/{customer_id}")
def update_customer_endpoint(customer_id: int, customer: Customer):
    updated_customer = update_customer(customer_id, customer)

    if updated_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return updated_customer

@app.post("/customers")
def create_customer_endpoint(customer: Customer):
    return create_customer(customer)

@app.get("/customers")
def get_customers():
    return get_all_customers()

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    customer = get_customer_by_id(customer_id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return dict(customer)