from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_customers(test_database):
    response = client.get("/customers")

    assert response.status_code == 200

    customers = response.json()

    assert isinstance(customers, list)

    for customer in customers:
        assert "id" in customer
        assert "name" in customer
        assert "email" in customer
        assert "phone" in customer


def test_get_customer_not_found(test_database):
    response = client.get("/customers/55")

    assert response.status_code == 404

    returned_response = response.json()

    assert returned_response == {
        "detail": "Customer not found"
    }

def test_get_customer(test_database):
    new_customer = {
        "name": "Customer To Get",
        "email": "get@example.com",
        "phone": "555-4444"
    }

    create_response = client.post(
        "/customers",
        json=new_customer
    )

    customer_id = create_response.json()["id"]

    response = client.get(f"/customers/{customer_id}")

    assert response.status_code == 200

    customer = response.json()

    assert customer["id"] == 1
    assert "name" in customer
    assert "email" in customer
    assert "phone" in customer

def test_create_customer(test_database, example_customer):
    response = client.post("/customers", json=example_customer)

    assert response.status_code == 200

    created_customer = response.json()

    assert created_customer["id"] is not None
    assert created_customer["name"] == "Test Customer"
    assert created_customer["email"] == "test@example.com"
    assert created_customer["phone"] == "555-0000"

def test_update_customer(test_database):
    new_customer = {
        "name": "Customer Before Update",
        "email": "before@example.com",
        "phone": "555-1111"
    }

    create_response = client.post(
        "/customers",
        json=new_customer
    )

    customer_id = create_response.json()["id"]

    updated_customer = {
        "name": "Customer After Update",
        "email": "after@example.com",
        "phone": "555-2222"
    }

    response = client.patch(
        f"/customers/{customer_id}",
        json=updated_customer
    )

    assert response.status_code == 200

    customer = response.json()

    assert customer["id"] == customer_id
    assert customer["name"] == "Customer After Update"
    assert customer["email"] == "after@example.com"
    assert customer["phone"] == "555-2222"

def test_update_customer_not_found(test_database):
    updated_customer = {
        "name": "Does Not Exist",
        "email": "doesnotexist@example.com",
        "phone": "555-9999"
    }

    response = client.patch(
        "/customers/999999",
        json=updated_customer
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found"
    }

def test_delete_customer(test_database):
    new_customer = {
        "name": "Customer To Delete",
        "email": "delete@example.com",
        "phone": "555-3333"
    }

    create_response = client.post(
        "/customers",
        json=new_customer
    )

    customer_id = create_response.json()["id"]

    response = client.delete(
        f"/customers/{customer_id}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Customer deleted"
    }

    get_response = client.get(
        f"/customers/{customer_id}"
    )

    assert get_response.status_code == 404

def test_delete_customer_not_found(test_database):
    response = client.delete("/customers/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found"
    }

def test_create_customer_missing_email(test_database):
    customer = {
        "name": "Test Customer",
        "phone": "555-0000"
    }

    response = client.post(
        "/customers",
        json=customer
    )

    assert response.status_code == 422


def test_create_customer_missing_name(test_database):
    customer = {
        "email": "test@example.com",
        "phone": "555-0000"
    }

    response = client.post(
        "/customers",
        json=customer
    )

    assert response.status_code == 422


def test_create_customer_missing_phone(test_database):
    customer = {
        "name": "Test Customer",
        "email": "test@example.com"
    }

    response = client.post(
        "/customers",
        json=customer
    )

    assert response.status_code == 422

def test_create_customer_invalid_name_type(test_database):
    customer = {
        "name": 123,
        "email": "test@example.com",
        "phone": "555-0000"
    }

    response = client.post(
        "/customers",
        json=customer
    )

    assert response.status_code == 422


def test_create_customer_invalid_email_type(test_database):
    customer = {
        "name": "Test Customer",
        "email": 123,
        "phone": "555-0000"
    }

    response = client.post(
        "/customers",
        json=customer
    )

    assert response.status_code == 422

def test_create_customer_invalid_phone_type(test_database):
    customer = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": 123
    }

    response = client.post(
        "/customers",
        json=customer
    )

    assert response.status_code == 422