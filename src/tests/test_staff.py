import pytest
from starlite.status_codes import HTTP_200_OK, HTTP_201_CREATED
from starlite.testing import TestClient

from ..main import app


test_client = TestClient(app=app)

test_data = [
    {"id": 1, "name": "Chief Commander", "post": "CEO"},
    {"id": 2, "name": "Legal Warrior", "post": "CLO"},
    {"id": 3, "name": "Money Maker", "post": "CFO"},
    {"id": 4, "name": "Nuts von Bolts", "post": "CAO"},
    {"id": 5, "name": "Luke Skywalker", "post": "CTO"}]


def test_employees_list():
    with test_client:
        clear_employees(test_client)
        check_create_employee(test_client)
        check_employees(test_client)
        check_employee_details(test_client)


def clear_employees(client: TestClient):
    response = client.get("/employees/delete/")


def check_employees(client: TestClient):
    response = client.get("/employees/")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == len(test_data)
    assert response.json()[-1] == test_data[-1]


def check_employee_details(client: TestClient):
    response = client.get("/employees/1/")
    assert response.status_code == HTTP_200_OK
    assert response.json()[0] == test_data[0]


def check_create_employee(client: TestClient):
    for record in test_data:
        response = client.post("/employees/", json=record)
        assert response.status_code == HTTP_201_CREATED
        assert response.json() == record
