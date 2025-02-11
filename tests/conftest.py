from datetime import UTC
from datetime import datetime
from uuid import uuid4

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from autoexpense3.models.expense import Expense
from autoexpense3.web_app.app import application as _application
from autoexpense3.web_app.application import Application
from tests.deployed_stagging.add_expense_test import DATE_FORMAT

fake = Faker()


def build_expense() -> Expense:
    return Expense(
        uuid=uuid4(),
        timestamp=datetime.strptime(
            fake.date(pattern=DATE_FORMAT), DATE_FORMAT
        ).replace(tzinfo=UTC),
        seller=fake.name(),
        total=float(fake.pricetag().replace(",", "").strip("$")),
    )


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
    return build_expense()


@pytest.fixture
def expense2() -> Expense:
    return build_expense()
