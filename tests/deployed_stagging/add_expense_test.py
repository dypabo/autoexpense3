from datetime import UTC
from datetime import datetime
from time import sleep
from uuid import UUID

import pytest
from faker import Faker
from playwright.sync_api import Locator
from playwright.sync_api import Page
from playwright.sync_api import expect

from autoexpense3.models.expense import Expense
from tests.utilities import DATE_FORMAT
from tests.utilities import build_expense

BUTTON = "new_expense_button"
DATE = "new_expense_date"
SELLER = "new_expense_seller"
TOTAL = "new_expense_total"
UUID_CLASS = "new_expense_uuid"


fake = Faker()


@pytest.mark.parametrize("field", [SELLER, DATE, TOTAL, BUTTON])
def test_page_has_new_expense_form(homepage: Page, field: str) -> None:
    expect(homepage.locator(f"#{field}")).to_be_visible(timeout=1)


def add_expense_to_page(page: Page, expense: Expense) -> None:
    page.locator(f"#{UUID_CLASS}").fill(str(expense.uuid))
    page.locator(f"#{DATE}").fill(expense.timestamp.strftime(DATE_FORMAT))
    page.locator(f"#{SELLER}").fill(expense.seller)
    page.locator(f"#{TOTAL}").fill(str(expense.total))
    page.locator(f"#{BUTTON}").click()
    page.reload()


def build_expense_from_expense_line(expense: Locator) -> Expense:
    uuid_str = expense.locator(".uuid").first.text_content()
    date_str = expense.locator(".date").first.text_content()
    total_str = expense.locator(".total").first.text_content()
    seller_str = expense.locator(".seller").first.text_content()
    if uuid_str is None or date_str is None or total_str is None or seller_str is None:
        raise ValueError
    uuid = UUID(uuid_str)
    date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=UTC)
    total = float(total_str.strip("$"))
    return Expense(uuid=uuid, timestamp=date, seller=seller_str, total=total)


def delete_expense_in_page(page: Page, expense: Expense) -> None:
    page.reload()
    for expense_line in page.locator(".expense").all():
        current_expense = build_expense_from_expense_line(expense_line)
        if (
            current_expense.to_expense_without_uuid()
            == expense.to_expense_without_uuid()
        ):
            expense_line.locator(".delete").first.click()
            page.reload()
            return
    raise ValueError


def get_expense_from_page(page: Page, expense: Expense) -> Expense:
    for expense_line in page.locator(".expense").all():
        current_expense = build_expense_from_expense_line(expense_line)
        if (
            current_expense.to_expense_without_uuid()
            == expense.to_expense_without_uuid()
        ):
            return current_expense
    raise ValueError


def expense_in_page(page: Page, expense: Expense) -> bool:
    try:
        get_expense_from_page(page, expense)
    except ValueError:
        return False
    return True


def test_added_expense_are_in_repository(homepage: Page) -> None:
    expense = build_expense()
    number_of_expense = homepage.locator(".expense").count()
    assert not expense_in_page(homepage, expense)
    add_expense_to_page(homepage, expense)
    assert homepage.locator(".expense").count() == number_of_expense + 1
    assert expense_in_page(homepage, expense)


def test_deleted_expense_are_not_in_repository(homepage: Page) -> None:
    expense = build_expense()
    add_expense_to_page(homepage, expense)
    number_of_expense = homepage.locator(".expense").count()
    assert expense_in_page(homepage, expense)
    delete_expense_in_page(homepage, expense)
    sleep(2)
    assert homepage.locator(".expense").count() == number_of_expense - 1
    assert not expense_in_page(homepage, expense)
