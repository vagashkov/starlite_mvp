from starlite.status_codes import HTTP_200_OK
from starlite.testing import TestClient

from ..main import app


def test_employees_list(test_client: TestClient):
    with TestClient(app=app) as client:
        response = client.get("/employees/")
        assert response.status_code == HTTP_200_OK
        assert len(response.json()) == 5
        assert response.json()[-1]["name"] == "Chair fon Table"

        test_data = [{"id": 1, 'post': "CEO", 'name': "Ivan Marakasoff"}]
        response = client.get("/employees/1/")
        assert response.status_code == HTTP_200_OK
        assert response.json() == test_data

