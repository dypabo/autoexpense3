from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID


@dataclass
class Expense:
    """Representation of an basic expense."""

    uuid: UUID
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
