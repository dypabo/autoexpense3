from datetime import UTC
from datetime import datetime

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from autoexpense3.models.expense import Expense
from autoexpense3.web_app.app import application as _application
from autoexpense3.web_app.application import Application
from tests.deployed_stagging.add_expense_test import DATE_FORMAT

fake = Faker()


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


@pytest.fixture
def expense() -> Expense:
    return Expense(
        datetime.strptime(fake.date(pattern=DATE_FORMAT), DATE_FORMAT).replace(
            tzinfo=UTC
        ),
        fake.name(),
        float(fake.pricetag().replace(",", "").strip("$")),
    )
