from fastapi.testclient import TestClient

from autoexpense3.web_app.constants import APP_NAME
from tests.utilities_html import get_webpage_title


def test_homepage_response_code_is_ok(client: TestClient) -> None:
    assert client.get("/").is_success


def test_app_name_in_homepage_title(homepage_content: str) -> None:
    assert APP_NAME in get_webpage_title(homepage_content)
