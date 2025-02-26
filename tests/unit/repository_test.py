# ruff: noqa: PLR6301

from contextlib import suppress
from autoexpense3.models.expense import Expense
from autoexpense3.models.user import User
from autoexpense3.models.repository import (
    Repository,
    UserNotFoundError,
    UserExistsError,
)
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


class TestUserRepository:
    """Tests for repository user related methods."""

    def test_raise_when_user_does_not_exists(
        self, user1: User, repo: Repository
    ) -> None:
        with suppress(UserNotFoundError):
            repo.get_user(user1.uuid)

    def test_can_add_user(self, user1: User, repo: Repository) -> None:
        repo.add_user(user1)
        assert user1 == repo.get_user(user1.uuid)

    def test_can_not_add_user_if_exists(self, user1: User, repo: Repository) -> None:
        repo.add_user(user1)
        with suppress(UserExistsError):
            repo.add_user(user1)
