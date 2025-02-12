import pytest
from fastapi.testclient import TestClient

from autoexpense3.models.expense import Expense
from autoexpense3.web_app.app import application as _application
from autoexpense3.web_app.application import Application
from tests.utilities import build_expense


@pytest.fixture
def application(expense: Expense, expense2: Expense) -> Application:
    _application.repository.add_expense(expense)
    _application.repository.add_expense(expense2)
    return _application


@pytest.fixture
def client(application: Application) -> TestClient:
    return TestClient(application.app)


@pytest.fixture
def homepage_content(client: TestClient) -> str:
    response = client.get("/")
    return str(response.content)


@pytest.fixture
def expense() -> Expense:
    return build_expense()


@pytest.fixture
def expense2() -> Expense:
    return build_expense()
