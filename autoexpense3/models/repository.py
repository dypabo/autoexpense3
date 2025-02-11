from abc import ABC
from abc import abstractmethod
from typing import TypedDict
from uuid import UUID

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

    @abstractmethod
    def remove_expense(self, uuid: UUID) -> None:
        """Remove expense to the repository."""


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

    def remove_expense(self, uuid: UUID) -> None:
        """Remove expense to the repository."""
        expenses = [e for e in self._data["expenses"] if e.uuid == uuid]
        expense = expenses[0]
        self._data["expenses"].remove(expense)

    def __repr__(self) -> str:
        """Return string representation of the RepositoryDict instance."""
        return str(self._data)
