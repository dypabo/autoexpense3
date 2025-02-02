from datetime import UTC
from datetime import datetime

from autoexpense3.models.expense import Expense
from autoexpense3.models.repository import RepositoryDict
from autoexpense3.web_app.app_builder import make_application

application = make_application(RepositoryDict())

application.repository.add_expense(
    Expense(
        datetime.strptime("2025-01-24", "%Y-%m-%d").astimezone(UTC),
        "gas station 123",
        60.00,
    ),
)
application.repository.add_expense(
    Expense(
        datetime.strptime("2025-01-24", "%Y-%m-%d").astimezone(UTC),
        "gas station 321",
        65.00,
    ),
)
app = application.fastapi
