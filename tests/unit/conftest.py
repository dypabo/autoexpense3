import pytest

from autoexpense3.models.expense import Expense
from autoexpense3.models.repository import Repository
from autoexpense3.models.repository import RepositoryDict


@pytest.fixture
def empty_repo() -> RepositoryDict:
    return RepositoryDict()


@pytest.fixture
def repo(empty_repo: RepositoryDict, expense: Expense, expense2: Expense) -> Repository:
    new_repo = empty_repo
    new_repo._data["expenses"].append(expense)  # noqa: SLF001  # pylint: disable=protected-access
    new_repo._data["expenses"].append(expense2)  # noqa: SLF001  # pylint: disable=protected-access
    return new_repo
