from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

from autoexpense3.models.expense import Expense
from autoexpense3.web_app.constants import APP_NAME

environment = Environment(
    loader=FileSystemLoader("autoexpense3/web_app/templates"),
    autoescape=True,
)

expenses = [
    Expense(datetime.strptime("2025-01-24", "%Y-%m-%d").astimezone(UTC), 60.00),
    Expense(datetime.strptime("2025-01-24", "%Y-%m-%d").astimezone(UTC), 65.00),
]


def homepage(request: Request) -> HTMLResponse:
    """Homepage route request processor."""
    _ = request
    homepage_template = environment.get_template("homepage.html")
    rendered_template = homepage_template.render(app_name=APP_NAME, expenses=expenses)
    return HTMLResponse(rendered_template)


def builder() -> FastAPI:
    """Return a FastAPI application."""
    app = FastAPI()
    app.add_route("/", homepage, methods=["get"])

    return app
