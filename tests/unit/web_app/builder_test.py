from datetime import UTC
from datetime import datetime

import pytest
import requests
from fastapi.testclient import TestClient

from autoexpense3.models.expense import Expense
from autoexpense3.models.repository import RepositoryDict
from autoexpense3.web_app.app_builder import make_application
from autoexpense3.web_app.application import Application
from autoexpense3.web_app.constants import APP_NAME
from tests.system.utilities import get_webpage_expenses
from tests.system.utilities import get_webpage_title


@pytest.fixture
def application() -> Application:
    app = make_application(RepositoryDict())
    app.repository.add_expenses(
        Expense(datetime.strptime("2025-01-24", "%Y-%m-%d").astimezone(UTC), 60.00),
    )
    app.repository.add_expenses(
        Expense(datetime.strptime("2025-01-24", "%Y-%m-%d").astimezone(UTC), 65.00),
    )
    return app


@pytest.fixture
def client(application: Application) -> TestClient:
    return TestClient(application.fastapi)


@pytest.fixture
def homepage_content(client: TestClient) -> str:
    response = client.get("/")
    return str(response.content)


def test_homepage_response_code_is_ok(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == requests.codes.get("ok")


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
