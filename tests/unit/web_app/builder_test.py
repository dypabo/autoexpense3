from fastapi.testclient import TestClient
from pytest import fixture

from autoexpense3.web_app.app_builder import builder
from autoexpense3.web_app.constants import APP_NAME
from tests.system.utilities import get_webpage_title


@fixture
def app():
    return builder()


@fixture
def client(app):
    return TestClient(app)


def test_app_name_in_homepage_title(client):
    response = client.get("/")
    assert response.status_code == 200
    assert APP_NAME in get_webpage_title(response.content)
