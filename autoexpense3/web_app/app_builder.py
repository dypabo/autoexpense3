from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment
from jinja2 import FileSystemLoader

from autoexpense3.models.repository import Repository
from autoexpense3.web_app.application import Application
from autoexpense3.web_app.constants import APP_NAME

application: Application | None = None

environment = Environment(
    loader=FileSystemLoader("autoexpense3/web_app/templates"),
    autoescape=True,
)


def homepage(request: Request) -> HTMLResponse:
    """Homepage route request processor."""
    _ = request
    homepage_template = environment.get_template("homepage.html")
    expenses = []
    if application is not None:
        expenses = application.repository.get_expenses()
    rendered_template = homepage_template.render(app_name=APP_NAME, expenses=expenses)
    return HTMLResponse(rendered_template)


def make_fastapi() -> FastAPI:
    """Return a FastAPI application."""
    app = FastAPI()
    app.add_route("/", homepage, methods=["get"])
    return app


def make_application(repository: Repository) -> Application:
    """Return an Application."""
    global application  # noqa: PLW0603  # pylint: disable=global-statement
    if application is None:
        application = Application(make_fastapi(), repository)
    return application
