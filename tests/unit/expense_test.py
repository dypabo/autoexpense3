from autoexpense3.models.expense import Expense


def test_expense_has_uuid_attribute(expense: Expense) -> None:
    assert hasattr(expense, "uuid")
