from abc import ABC
from abc import abstractmethod
from typing import TypedDict
from uuid import UUID

from autoexpense3.models.expense import Expense


class RepoDataDict(TypedDict):
    """Data container for the RepositoryDict."""

    expenses: dict[UUID, Expense]


class Repository(ABC):
    """Base class for Repository."""

    @abstractmethod
    def get_expenses(self) -> list[Expense]:
        """Return expenses from repository."""

    @abstractmethod
    def get_expense(self, uuid: UUID) -> Expense:
        """Return expense from repository."""

    @abstractmethod
    def edit_expense(self, expense: Expense) -> None:
        """Return expense from repository."""

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
            "expenses": {},
        }

    def get_expenses(self) -> list[Expense]:
        """Return expenses from repository."""
        return list(self._data["expenses"].values())

    def get_expense(self, uuid: UUID) -> Expense:
        """Return expense from repository."""
        return self._data["expenses"][uuid]

    def edit_expense(self, expense: Expense) -> None:
        """Return expense from repository."""
        self._data["expenses"][expense.uuid] = expense

    def add_expense(self, expense: Expense) -> None:
        """Add expense to the repository."""
        self._data["expenses"][expense.uuid] = expense

    def remove_expense(self, uuid: UUID) -> None:
        """Remove expense to the repository."""
        del self._data["expenses"][uuid]

    def __repr__(self) -> str:
        """Return string representation of the RepositoryDict instance."""
        return str(self._data)
