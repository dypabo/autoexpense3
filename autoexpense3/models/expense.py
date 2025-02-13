from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID


@dataclass
class ExpenseNoUuid:
    """Representation of an basic expense without UUID."""

    timestamp: datetime
    seller: str
    # TODO(Jason): replace py proper type for money
    # https://github.com/dypabo/autoexpense3/issues/1
    total: float

    def jsonify(self) -> dict:
        """Return a JSON representation of this instance."""
        return {
            "timestamp": str(self.timestamp),
            "seller": self.seller,
            "total": self.total,
        }


@dataclass
class Expense(ExpenseNoUuid):
    """Representation of an basic expense."""

    uuid: UUID

    def jsonify(self) -> dict:
        """Return a JSON representation of this instance."""
        json = super().jsonify()
        json["uuid"] = self.uuid
        return json

    def to_expense_without_uuid(self) -> ExpenseNoUuid:
        """Return a ExpenseNoUuid object with data from self."""
        return ExpenseNoUuid(self.timestamp, self.seller, self.total)
