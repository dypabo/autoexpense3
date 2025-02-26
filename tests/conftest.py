import subprocess  # noqa: S404
import time
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from autoexpense3.models.expense import Expense
from autoexpense3.models.user import User
from autoexpense3.web_app.app import application as _application
from autoexpense3.web_app.application import Application
from tests.utilities import build_expense
from tests.utilities import build_user
from tests.utilities import kill_process_and_children


@pytest.fixture(scope="session")
def real_web_application() -> Generator[None, None, None]:
    cmd = "uv run fastapi dev"
    with subprocess.Popen(cmd, cwd=Path.cwd(), shell=True) as proc:  # noqa: S602
        time.sleep(3)
        yield
        kill_process_and_children(proc.pid)


@pytest.fixture
def url() -> str:
    return "http://127.0.0.1:8000"


@pytest.fixture
def application(expense: Expense, expense2: Expense) -> Application:
    _application.repository.add_expense(expense)
    _application.repository.add_expense(expense2)
    return _application


@pytest.fixture
def client(application: Application) -> TestClient:
    return TestClient(application.app)


@pytest.fixture
def user_expenses_content(client: TestClient) -> str:
    response = client.get("/user")
    return str(response.content)


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


@pytest.fixture
def user1() -> User:
    return build_user()


@pytest.fixture
def user2() -> User:
    return build_user()
