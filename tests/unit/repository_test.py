import pytest

from autoexpense3.models.expense import Expense
from autoexpense3.models.repository import Repository
from autoexpense3.models.repository import RepositoryDict


@pytest.fixture
def repo() -> RepositoryDict:
    return RepositoryDict()


def test_repo_has_no_expense_at_creation(repo: Repository) -> None:
    assert len(repo.get_expenses()) == 0


def test_repo_return_expenses(repo: RepositoryDict, expense: Expense) -> None:
    repo._data["expenses"].append(expense)  # noqa: SLF001  # pylint: disable=protected-access
    assert len(repo.get_expenses()) == 1
    assert repo.get_expenses()[0] == expense


def test_can_add_expense_to_repository(repo: Repository, expense: Expense) -> None:
    assert len(repo.get_expenses()) == 0
    repo.add_expense(expense)
    assert len(repo.get_expenses()) == 1
    assert repo.get_expenses()[0] == expense
