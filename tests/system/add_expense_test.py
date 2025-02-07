from datetime import UTC
from datetime import datetime

import pytest
from faker import Faker
from playwright.sync_api import Page
from playwright.sync_api import expect

from autoexpense3.models.expense import Expense
from autoexpense3.web_app.application import Application

BUTTON = "new_expense_button"
DATE = "new_expense_date"
SELLER = "new_expense_seller"
TOTAL = "new_expense_total"

DATE_FORMAT = "%Y-%m-%d"

fake = Faker()


@pytest.fixture
def expense() -> Expense:
    return Expense(
        datetime.strptime(fake.date(pattern=DATE_FORMAT), DATE_FORMAT).replace(
            tzinfo=UTC
        ),
        fake.name(),
        float(fake.pricetag().replace(",", "").strip("$")),
    )


@pytest.mark.parametrize("field", [SELLER, DATE, TOTAL, BUTTON])
def test_page_has_new_expense_form(homepage: Page, field: str) -> None:
    expect(homepage.locator(f"#{field}")).to_be_visible(timeout=1)


def test_add_expense_are_in_repository(
    homepage: Page, application: Application, expense: Expense
) -> None:
    number_of_expense = len(application.repository.get_expenses())
    homepage.locator(f"#{DATE}").fill(expense.timestamp.strftime(DATE_FORMAT))
    homepage.locator(f"#{SELLER}").fill(expense.seller)
    homepage.locator(f"#{TOTAL}").fill(str(expense.total))
    homepage.locator(f"#{BUTTON}").click()

    assert homepage.locator(".expense").count() == number_of_expense + 1
    expect(homepage.locator(".expense .date").last).to_have_text(
        expense.timestamp.strftime("%Y-%m-%d")
    )
    expect(homepage.locator(".expense .seller").last).to_have_text(expense.seller)
    expect(homepage.locator(".expense .total").last).to_have_text(
        f"{expense.total:.02f}$"
    )
