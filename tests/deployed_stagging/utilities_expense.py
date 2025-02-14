from datetime import UTC
from datetime import datetime
from uuid import UUID

from playwright.sync_api import Locator
from playwright.sync_api import Page

from autoexpense3.models.expense import Expense
from tests.utilities import DATE_FORMAT

BUTTON = "expense_button"
DATE = "expense_date"
SELLER = "expense_seller"
TOTAL = "expense_total"


def add_expense_to_page(page: Page, expense: Expense) -> None:
    """Add an expense with the web page."""
    page.locator(f"#new_{DATE}").fill(expense.timestamp.strftime(DATE_FORMAT))
    page.locator(f"#new_{SELLER}").fill(expense.seller)
    page.locator(f"#new_{TOTAL}").fill(str(expense.total))
    page.locator(f"#new_{BUTTON}").click()
    page.reload()


def _build_expense_from_expense_line(expense: Locator) -> Expense:
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
    """Delete an expense with the web page."""
    page.reload()
    for expense_line in page.locator(".expense").all():
        current_expense = _build_expense_from_expense_line(expense_line)
        if current_expense.uuid == expense.uuid:
            expense_line.locator(".delete").first.click()
            page.reload()
            return
    raise ValueError


def edit_expense_in_page(page: Page, expense: Expense) -> None:
    """Modify an expense with the web page."""
    page.reload()
    target_uuid = expense.uuid
    for expense_line in page.locator(".expense").all():
        current_expense = _build_expense_from_expense_line(expense_line)
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


def _get_expense_from_page(page: Page, expense: Expense) -> Expense:
    """Get the expense from the page."""
    for expense_line in page.locator(".expense").all():
        current_expense = _build_expense_from_expense_line(expense_line)
        if (
            current_expense.to_expense_without_uuid()
            == expense.to_expense_without_uuid()
        ):
            return current_expense
    raise ValueError


def expense_in_page(page: Page, expense: Expense) -> bool:
    """Validate the presence of an expense in page."""
    try:
        _get_expense_from_page(page, expense)
    except ValueError:
        return False
    return True


def get_number_of_expense_on_page(homepage: Page) -> int:
    """Parse homepage to extract the number of expenses."""
    homepage.reload()
    return int(homepage.locator(".expense").count())
