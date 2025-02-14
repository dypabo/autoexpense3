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

BUTTON = "expense_button"
DATE = "expense_date"
SELLER = "expense_seller"
TOTAL = "expense_total"


fake = Faker()


@pytest.mark.parametrize(
    "field", [f"new_{SELLER}", f"new_{DATE}", f"new_{TOTAL}", f"new_{BUTTON}"]
)
def test_page_has_new_expense_form(homepage: Page, field: str) -> None:
    expect(homepage.locator(f"#{field}")).to_be_visible(timeout=1)


def add_expense_to_page(page: Page, expense: Expense) -> None:
    page.locator(f"#new_{DATE}").fill(expense.timestamp.strftime(DATE_FORMAT))
    page.locator(f"#new_{SELLER}").fill(expense.seller)
    page.locator(f"#new_{TOTAL}").fill(str(expense.total))
    page.locator(f"#new_{BUTTON}").click()
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


def edit_expense_in_page(page: Page, expense: Expense) -> None:
    target_uuid = expense.uuid
    for expense_line in page.locator(".expense").all():
        current_expense = build_expense_from_expense_line(expense_line)
        if current_expense.uuid != target_uuid:
            continue
        expense_line.locator(".edit").first.click()
        page.locator(f"#edit_{DATE}").fill(expense.timestamp.strftime(DATE_FORMAT))
        page.locator(f"#edit_{SELLER}").fill(expense.seller)
        page.locator(f"#edit_{TOTAL}").fill(str(expense.total))
        page.locator(f"#edit_{BUTTON}").click()
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


def test_edited_expense_are_listed_in_expense_report_page(homepage: Page) -> None:
    existing_expense = build_expense()
    add_expense_to_page(homepage, existing_expense)
    number_of_expense = homepage.locator(".expense").count()
    assert expense_in_page(homepage, existing_expense)
    existing_expense = get_expense_from_page(
        homepage, existing_expense
    )  # get real uuid

    modified_expense = build_expense()
    modified_expense.uuid = existing_expense.uuid

    edit_expense_in_page(homepage, modified_expense)
    sleep(2)
    assert homepage.locator(".expense").count() == number_of_expense
    assert not expense_in_page(homepage, existing_expense)
    assert expense_in_page(homepage, modified_expense)
