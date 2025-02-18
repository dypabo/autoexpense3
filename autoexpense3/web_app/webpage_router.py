from datetime import UTC
from datetime import datetime
from os import environ

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from autoexpense3.web_app.application import Application
from autoexpense3.web_app.constants import APP_NAME
from autoexpense3.web_app.constants import APP_URL


def build_webpage_router(application: Application) -> APIRouter:
    """Build application router."""
    webpage_router = APIRouter()

    @webpage_router.get("/")
    def homepage(request: Request) -> HTMLResponse:
        """Homepage route request processor."""
        context = {
            "app_name": APP_NAME,
        }
        return application.templates.TemplateResponse(
            request=request,
            name="homepage.html",
            context=context,
        )

    @webpage_router.get("/user")
    def user(request: Request) -> HTMLResponse:
        """User route request processor."""
        expenses = application.repository.get_expenses()
        app_url = "http://127.0.0.1:8000"
        if environ.get("GITHUB") or not environ.get("PYTEST_VERSION"):
            app_url = APP_URL
        context = {
            "app_name": APP_NAME,
            "app_url": app_url,
            "expenses": expenses,
            "today": datetime.now(tz=UTC),
        }
        return application.templates.TemplateResponse(
            request=request,
            name="expenses.html",
            context=context,
        )

    _ = user
    _ = homepage
    return webpage_router
