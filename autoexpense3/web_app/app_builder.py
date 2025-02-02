from datetime import UTC
from datetime import datetime
from typing import Annotated

from fastapi import FastAPI
from fastapi import Form
from fastapi import Header
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from jinja2 import Environment
from jinja2 import FileSystemLoader

from autoexpense3.models.expense import Expense
from autoexpense3.models.repository import Repository
from autoexpense3.web_app.application import Application
from autoexpense3.web_app.constants import APP_NAME

application: Application | None = None

environment = Environment(
    loader=FileSystemLoader("autoexpense3/web_app/templates"),
    autoescape=True,
)

app = FastAPI()
templates = Jinja2Templates(directory="autoexpense3/web_app/templates")


@app.get("/expenses")
def expenses(hx_request: Annotated[str | None, Header] = None) -> Response:
    """Get a list of expenses from application repository."""
    if application is None:
        return JSONResponse("")
    if hx_request:
        return HTMLResponse("")
    return JSONResponse([e.jsonify() for e in application.repository.get_expenses()])


@app.post("/new_expense")
def new_expense(
    request: Request,
    new_expense_date: Annotated[str, Form()],
    new_expense_seller: Annotated[str, Form()],
    new_expense_total: Annotated[float, Form()],
) -> Response:
    """Add new expense endpoint."""
    if application is None:
        return JSONResponse("")
    date = f"{new_expense_date}:{UTC}"
    expense = Expense(
        datetime.strptime(date, "%Y-%m-%d:%Z").replace(tzinfo=UTC),
        new_expense_seller,
        new_expense_total,
    )
    application.repository.add_expense(expense)
    return templates.TemplateResponse(
        request=request, name="expenses.html", context={"expense": expense}
    )


@app.get("/")
def homepage(request: Request) -> HTMLResponse:
    """Homepage route request processor."""
    _ = request
    homepage_template = environment.get_template("homepage.html")
    expenses = []
    if application is not None:
        expenses = application.repository.get_expenses()
    rendered_template = homepage_template.render(
        app_name=APP_NAME,
        expenses=expenses,
        today=datetime.now(tz=UTC),
    )
    return HTMLResponse(rendered_template)


def make_fastapi() -> FastAPI:
    """Return a FastAPI application."""
    return app


def make_application(repository: Repository) -> Application:
    """Return an Application."""
    global application  # noqa: PLW0603  # pylint: disable=global-statement
    if application is None:
        application = Application(make_fastapi(), repository)
    return application
