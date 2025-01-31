from fastapi.testclient import TestClient

from autoexpense3.web_app.application import Application
from autoexpense3.web_app.constants import APP_NAME
from tests.system.utilities import get_webpage_expenses
from tests.system.utilities import get_webpage_title


def test_homepage_response_code_is_ok(client: TestClient) -> None:
    assert client.get("/").is_success


def test_app_name_in_homepage_title(homepage_content: str) -> None:
    assert APP_NAME in get_webpage_title(homepage_content)


def test_homepage_has_expenses_section(
    homepage_content: str, application: Application
) -> None:
    webpage_expenses = get_webpage_expenses(homepage_content)
    expenses = application.repository.get_expenses()
    assert len(webpage_expenses) == len(expenses)
    assert webpage_expenses[0] == expenses[0]
    assert webpage_expenses[1] == expenses[1]
