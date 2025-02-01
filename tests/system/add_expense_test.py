import pytest
from playwright.sync_api import Page
from playwright.sync_api import expect

SELLER = "new_expense_seller"
DATE = "new_expense_date"
TOTAL = "new_expense_total"
BUTTON = "new_expense_button"


@pytest.mark.parametrize("field", [SELLER, DATE, TOTAL, BUTTON])
def test_page_has_new_expense_form(homepage: Page, field: str) -> None:
    expect(homepage.locator(f"#{field}")).to_be_visible(timeout=1)
