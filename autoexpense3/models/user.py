from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    """User data."""

    uuid: UUID
    username: str
    password: str
