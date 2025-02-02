from abc import ABC
from abc import abstractmethod
from typing import TypedDict

from autoexpense3.models.expense import Expense


class RepoDataDict(TypedDict):
    """Data container for the RepositoryDict."""

    expenses: list[Expense]


class Repository(ABC):
    """Base class for Repository."""

    @abstractmethod
    def get_expenses(self) -> list[Expense]:
        """Return expenses from repository."""

    @abstractmethod
    def add_expense(self, expense: Expense) -> None:
        """Add expense to the repository."""


class RepositoryDict(Repository):
    """Repository implementation with a dictionary."""

    def __init__(self) -> None:
        self._data: RepoDataDict = {
            "expenses": [],
        }

    def get_expenses(self) -> list[Expense]:
        """Return expenses from repository."""
        return self._data["expenses"]

    def add_expense(self, expense: Expense) -> None:
        """Add expense to the repository."""
        self._data["expenses"].append(expense)

    def __repr__(self) -> str:
        """Return string representation of the RepositoryDict instance."""
        return str(self._data)
