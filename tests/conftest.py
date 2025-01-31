from datetime import UTC
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from autoexpense3.models.expense import Expense
from autoexpense3.models.repository import Repository
from autoexpense3.models.repository import RepositoryDict
from autoexpense3.web_app.app_builder import make_application
from autoexpense3.web_app.application import Application


@pytest.fixture
def repository() -> RepositoryDict:
    repo = RepositoryDict()
    repo.add_expenses(
        Expense(datetime.strptime("2025-01-24", "%Y-%m-%d").astimezone(UTC), 60.00),
    )
    repo.add_expenses(
        Expense(datetime.strptime("2025-01-25", "%Y-%m-%d").astimezone(UTC), 65.00),
    )
    return repo


@pytest.fixture
def application(repository: Repository) -> Application:
    return make_application(repository)


@pytest.fixture
def client(application: Application) -> TestClient:
    return TestClient(application.fastapi)


@pytest.fixture
def homepage_content(client: TestClient) -> str:
    response = client.get("/")
    return str(response.content)
