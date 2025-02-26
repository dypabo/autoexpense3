from abc import ABC
from abc import abstractmethod
from typing import TypedDict
from uuid import UUID

from autoexpense3.models.expense import Expense
from autoexpense3.models.user import User


class RepoDataDict(TypedDict):
    """Data container for the RepositoryDict."""

    expenses: dict[UUID, Expense]
    users: dict[UUID, User]


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

    @abstractmethod
    def get_user(self, uuid: UUID) -> User:
        """Get user from the repository."""

    @abstractmethod
    def add_user(self, user: User) -> None:
        """Add user to the repository."""


class RepositoryDict(Repository):
    """Repository implementation with a dictionary."""

    def __init__(self) -> None:
        self._data: RepoDataDict = {
            "expenses": {},
            "users": {},
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

    def get_user(self, uuid: UUID) -> User:
        """Get user from the repository."""
        if uuid not in self._data["users"]:
            raise UserNotFoundError
        return self._data["users"][uuid]

    def add_user(self, user: User) -> None:
        """Add user to the repository."""
        self._data["users"][user.uuid] = user

    def __repr__(self) -> str:
        """Return string representation of the RepositoryDict instance."""
        return str(self._data)


class RepositoryError(Exception):
    """Module custom exception."""


class UserNotFoundError(RepositoryError):
    """Raised when user is not in the repository."""


class UserExistsError(RepositoryError):
    """Raised when user is already in the repository."""
