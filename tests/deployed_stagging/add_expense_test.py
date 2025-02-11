from datetime import UTC
from datetime import datetime

import pytest
from faker import Faker
from playwright.sync_api import Locator
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


@pytest.mark.parametrize("field", [SELLER, DATE, TOTAL, BUTTON])
def test_page_has_new_expense_form(homepage: Page, field: str) -> None:
    expect(homepage.locator(f"#{field}")).to_be_visible(timeout=1)


def add_expense_to_page(page: Page, expense: Expense) -> None:
    page.locator(f"#{DATE}").fill(expense.timestamp.strftime(DATE_FORMAT))
    page.locator(f"#{SELLER}").fill(expense.seller)
    page.locator(f"#{TOTAL}").fill(str(expense.total))
    page.locator(f"#{BUTTON}").click()


def build_expense_from_expense_line(expense: Locator) -> Expense:
    date_str = expense.locator(".date").first.text_content()
    total_str = expense.locator(".total").first.text_content()
    seller_str = expense.locator(".seller").first.text_content()
    if date_str is None or total_str is None or seller_str is None:
        raise ValueError
    date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=UTC)
    total = float(total_str.strip("$"))
    return Expense(timestamp=date, seller=seller_str, total=total)


def delete_expense_in_page(page: Page, expense: Expense) -> None:
    for expense_line in page.locator(".expense").all():
        current_expense = build_expense_from_expense_line(expense_line)
        if current_expense == expense:
            page.locator(".delete").first.click()
    raise ValueError


def get_expense_from_page(page: Page, expense: Expense) -> Expense:
    for expense_line in page.locator(".expense").all():
        current_expense = build_expense_from_expense_line(expense_line)
        if current_expense == expense:
            return current_expense
    raise ValueError


def expense_in_page(page: Page, expense: Expense) -> bool:
    try:
        get_expense_from_page(page, expense)
    except ValueError:
        return False
    return True


def test_added_expense_are_in_repository(
    homepage: Page, application: Application, expense: Expense
) -> None:
    number_of_expense = len(application.repository.get_expenses())
    add_expense_to_page(homepage, expense)
    assert homepage.locator(".expense").count() == number_of_expense + 1
    assert expense_in_page(homepage, expense)


def test_deleted_expense_are_not_in_repository(
    homepage: Page, application: Application, expense: Expense
) -> None:
    application.repository.add_expense(expense)
    number_of_expense = len(application.repository.get_expenses())
    homepage.reload()
    delete_expense_in_page(homepage, expense)
    assert homepage.locator(".expense").count() == number_of_expense - 1
    assert not expense_in_page(homepage, expense)
