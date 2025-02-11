from datetime import UTC
from datetime import datetime
from os import environ
from uuid import uuid4

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from autoexpense3.models.expense import Expense
from autoexpense3.models.repository import RepositoryDict
from autoexpense3.web_app.application import Application
from autoexpense3.web_app.expenses_router import build_expenses_router
from autoexpense3.web_app.webpage_router import build_webpage_router

_app = FastAPI()
_templates = Jinja2Templates("autoexpense3/web_app/templates")
_repository = RepositoryDict()

if environ.get("PYTEST_VERSION") is not None:
    _repository.add_expense(
        Expense(
            uuid4(),
            datetime.strptime("2026-01-24", "%Y-%m-%d").astimezone(UTC),
            "gas station 123",
            60.00,
        ),
    )
    _repository.add_expense(
        Expense(
            uuid4(),
            datetime.strptime("2026-01-24", "%Y-%m-%d").astimezone(UTC),
            "gas station 321",
            65.00,
        ),
    )
else:
    _repository.add_expense(
        Expense(
            uuid4(),
            datetime.strptime("2025-01-24", "%Y-%m-%d").astimezone(UTC),
            "gas station 123",
            60.00,
        ),
    )
    _repository.add_expense(
        Expense(
            uuid4(),
            datetime.strptime("2025-01-24", "%Y-%m-%d").astimezone(UTC),
            "gas station 321",
            65.00,
        ),
    )

application = Application(_app, _repository, _templates)
_app.include_router(build_expenses_router(application))
_app.include_router(build_webpage_router(application))
