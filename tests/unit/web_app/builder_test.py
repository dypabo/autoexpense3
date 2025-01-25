import pytest
import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient

from autoexpense3.web_app.app_builder import builder
from autoexpense3.web_app.constants import APP_NAME
from tests.system.utilities import get_webpage_title


@pytest.fixture
def app() -> FastAPI:
    return builder()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def homepage_content(client: TestClient) -> str:
    response = client.get("/")
    return str(response.content)


def test_homepage_response_code_is_ok(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == requests.codes.get("ok")


def test_app_name_in_homepage_title(homepage_content: str) -> None:
    assert APP_NAME in get_webpage_title(homepage_content)
