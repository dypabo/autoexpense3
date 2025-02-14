from collections.abc import Generator

import pytest
import requests
from playwright.sync_api import Page

from autoexpense3.models.expense import Expense
from tests.utilities import DATE_FORMAT


@pytest.fixture
def homepage(
    page: Page, url: str, real_web_application: Generator[None, None, None]
) -> Page:
    _ = real_web_application
    page.goto(url)
    return page


@pytest.fixture
def app_url() -> str:
    return "http://127.0.0.1:8000"


@pytest.fixture
def repo_with_expenses(
    app_url: str, repo_expenses: list[Expense], homepage: Page
) -> list[Expense]:
    for expense in repo_expenses:
        params = {"new_expense_uuid": str(expense.uuid)}
        data = {
            "new_expense_date": expense.timestamp.strftime(DATE_FORMAT),
            "new_expense_seller": expense.seller,
            "new_expense_total": expense.total,
        }
        resp = requests.post(
            f"{app_url}/api/v1/expenses?new_expense_uuid={expense.uuid}",
            data=data,
            params=params,
            timeout=2,
        )
        resp.raise_for_status()
    homepage.reload()
    return repo_expenses
