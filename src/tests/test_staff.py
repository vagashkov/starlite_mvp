from starlite.status_codes import HTTP_200_OK
from starlite.testing import TestClient

from ..main import app


test_client = TestClient(app=app)


def test_employees_list():
    with test_client:
        check_employees(test_client)
        check_employee_details(test_client)


def check_employees(client: TestClient):
    response = client.get("/employees/")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == 5
    assert response.json()[-1]["name"] == "Chair fon Table"


def check_employee_details(client: TestClient):
    test_data = [{"id": 1, 'post': "CEO", 'name': "Ivan Marakasoff"}]
    response = client.get("/employees/1/")
    assert response.status_code == HTTP_200_OK
    assert response.json() == test_data

