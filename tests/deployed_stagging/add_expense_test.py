import pytest
from playwright.sync_api import Page
from playwright.sync_api import expect

from autoexpense3.models.expense import Expense
from tests.deployed_stagging.utilities_expense import add_expense_to_page
from tests.deployed_stagging.utilities_expense import delete_expense_in_page
from tests.deployed_stagging.utilities_expense import edit_expense_in_page
from tests.deployed_stagging.utilities_expense import expense_in_page
from tests.deployed_stagging.utilities_expense import get_number_of_expense_on_page
from tests.utilities import build_expense

BUTTON = "expense_button"
DATE = "expense_date"
SELLER = "expense_seller"
TOTAL = "expense_total"


@pytest.mark.parametrize(
    "field", [f"new_{SELLER}", f"new_{DATE}", f"new_{TOTAL}", f"new_{BUTTON}"]
)
def test_page_has_new_expense_form(homepage: Page, field: str) -> None:
    expect(homepage.locator(f"#{field}")).to_be_visible(timeout=1)


def test_added_expense_are_in_repository(homepage: Page) -> None:
    expense = build_expense()
    number_of_expense = get_number_of_expense_on_page(homepage)
    assert not expense_in_page(homepage, expense)
    add_expense_to_page(homepage, expense)
    assert get_number_of_expense_on_page(homepage) == number_of_expense + 1
    assert expense_in_page(homepage, expense)


@pytest.mark.parametrize("repo_expenses", [(build_expense(),)])
@pytest.mark.usefixtures("repo_with_expenses")
def test_deleted_expense_are_not_in_repository(
    homepage: Page, repo_expenses: list[Expense]
) -> None:
    expense = repo_expenses[0]
    number_of_expense = get_number_of_expense_on_page(homepage)
    delete_expense_in_page(homepage, expense)
    assert get_number_of_expense_on_page(homepage) == number_of_expense - 1
    assert not expense_in_page(homepage, expense)


@pytest.mark.parametrize("repo_expenses", [(build_expense(),)])
@pytest.mark.usefixtures("repo_with_expenses")
def test_edited_expense_are_listed_in_expense_report_page(
    homepage: Page, repo_expenses: list[Expense]
) -> None:
    expense = repo_expenses[0]
    number_of_expense = get_number_of_expense_on_page(homepage)
    modified_expense = build_expense()
    modified_expense.uuid = expense.uuid
    edit_expense_in_page(homepage, modified_expense)
    assert get_number_of_expense_on_page(homepage) == number_of_expense
    assert not expense_in_page(homepage, expense)
    assert expense_in_page(homepage, modified_expense)
