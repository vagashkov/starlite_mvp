from starlite.status_codes import HTTP_200_OK
from starlite.testing import TestClient

from ..main import app


def test_employees_list(test_client: TestClient):
    with TestClient(app=app) as client:
        response = client.get("/employees")
        assert response.status_code == HTTP_200_OK
        assert len(response.json()['staff_list']) == 4
        assert response.json()['staff_list'][-1]['name'] == 'Giveme Moremoney'


def test_employee_details(test_client: TestClient):
    test_data = {"id": 1, 'post': "CEO", 'name': "Ivan Marakasoff"}
    with TestClient(app=app) as client:
        response = client.get("/employees/0")
        assert response.status_code == HTTP_200_OK
        assert response.json() == test_data
