from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

from autoexpense3.web_app.constants import APP_NAME

environment = Environment(
    loader=FileSystemLoader("autoexpense3/web_app/templates"),
    autoescape=True,
)


def homepage(request: Request) -> HTMLResponse:
    """Homepage route request processor."""
    _ = request
    homepage_template = environment.get_template("homepage.html")
    rendered_template = homepage_template.render(app_name=APP_NAME)
    return HTMLResponse(rendered_template)


def builder() -> FastAPI:
    """Return a FastAPI application."""
    app = FastAPI()
    app.add_route("/", homepage, methods=["get"])

    return app
