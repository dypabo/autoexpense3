import pytest
from fastapi.testclient import TestClient

from autoexpense3.web_app.app import application as _application
from autoexpense3.web_app.application import Application


@pytest.fixture
def application() -> Application:
    return _application


@pytest.fixture
def client(application: Application) -> TestClient:
    return TestClient(application.app)


@pytest.fixture
def homepage_content(client: TestClient) -> str:
    response = client.get("/")
    return str(response.content)
