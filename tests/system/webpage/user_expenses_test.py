from autoexpense3.web_app.application import Application
from tests.utilities_html import get_webpage_expenses


def test_homepage_has_expenses_section(
    user_expenses_content: str, application: Application
) -> None:
    webpage_expenses = get_webpage_expenses(user_expenses_content)
    expenses = application.repository.get_expenses()
    assert len(webpage_expenses) == len(expenses)
    assert webpage_expenses[0] == expenses[0]
    assert webpage_expenses[1] == expenses[1]
