from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class Expense:
    """Representation of an basic expense."""

    timestamp: datetime
    # TODO(Jason): replace py proper type for money
    # https://github.com/dypabo/autoexpense3/issues/1
    total: float
