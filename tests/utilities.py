from datetime import UTC
from datetime import datetime
from uuid import uuid4

import psutil
from faker import Faker

from autoexpense3.models.expense import Expense
from tests.deployed_stagging.add_expense_test import DATE_FORMAT

fake = Faker()


def build_expense() -> Expense:
    """Generate random expenses."""
    return Expense(
        uuid=uuid4(),
        timestamp=datetime.strptime(
            fake.date(pattern=DATE_FORMAT), DATE_FORMAT
        ).replace(tzinfo=UTC),
        seller=fake.name(),
        total=float(fake.pricetag().replace(",", "").strip("$")),
    )


def kill_process_and_children(pid: int) -> None:
    """Kill a process and all its children."""
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()
