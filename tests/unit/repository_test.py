from autoexpense3.models.expense import Expense
from autoexpense3.models.repository import Repository
from autoexpense3.models.repository import RepositoryDict


def test_repo_has_no_expense_at_creation(empty_repo: Repository) -> None:
    assert len(empty_repo.get_expenses()) == 0


def test_repo_return_expenses(
    repo: RepositoryDict, expense: Expense, expense2: Expense
) -> None:
    assert len(repo.get_expenses()) == len(repo._data["expenses"])  # noqa: SLF001  # pylint: disable=protected-access
    assert repo.get_expenses()[0] == expense
    assert repo.get_expenses()[1] == expense2


def test_can_add_expense_to_repository(
    empty_repo: Repository, expense: Expense
) -> None:
    repo = empty_repo
    number_of_expense = len(repo.get_expenses())
    repo.add_expense(expense)
    assert len(repo.get_expenses()) == number_of_expense + 1
    assert repo.get_expenses()[-1] == expense


def test_can_expense_from_repository(
    repo: Repository, expense: Expense, expense2: Expense
) -> None:
    number_of_expense = len(repo.get_expenses())
    repo.remove_expense(expense.uuid)
    assert len(repo.get_expenses()) == number_of_expense - 1
    assert expense2 in repo.get_expenses()
