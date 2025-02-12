from fastapi.testclient import TestClient

from autoexpense3.models.expense import Expense
from autoexpense3.web_app.application import Application


def test_can_remove_expense_from_expense_list(
    client: TestClient, application: Application, expense: Expense
) -> None:
    assert expense in application.repository.get_expenses()
    response = client.delete(f"/expenses/{expense.uuid}")
    assert response.is_success
    assert expense not in application.repository.get_expenses()
