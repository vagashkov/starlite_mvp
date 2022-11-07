from starlite.status_codes import HTTP_200_OK
from starlite.testing import TestClient

from ..main import app


def test_employees_list(test_client: TestClient):
    with TestClient(app=app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK
        assert response.json()['CEO'] == "Ivan Marakasoff"
