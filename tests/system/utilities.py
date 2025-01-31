from datetime import UTC
from datetime import datetime

from bs4 import BeautifulSoup
from bs4.element import Tag

from autoexpense3.models.expense import Expense


def _get_tags(html: str | Tag, tag: str) -> list[Tag]:
    if isinstance(html, str):
        html = BeautifulSoup(html, features="html.parser")
    tags = html.select(tag)
    return list(tags)


def _get_first_tag(html: str | Tag, tag: str) -> Tag:
    """In an HTML string, return the the first matching tag."""
    return _get_tags(html, tag)[0]


def get_webpage_title(html: str) -> str:
    """Return the webpage title string for an HTML string."""
    return _get_first_tag(html, "title").text


def get_webpage_expenses(html: str) -> list[Expense]:
    """Return the list of `expense`."""

    def build_expense(expense_html: str) -> Expense:
        date = datetime.strptime(
            _get_first_tag(expense_html, ".expense .date").text, "%Y-%m-%d"
        ).astimezone(UTC)
        total = float(_get_first_tag(expense_html, ".expense .total").text.strip("$"))
        return Expense(date, total)

    expenses = _get_tags(html, ".expense")
    return [build_expense(str(t)) for t in expenses]
