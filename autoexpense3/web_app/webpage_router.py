from datetime import UTC
from datetime import datetime

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
        expenses = application.repository.get_expenses()
        context = {
            "app_name": APP_NAME,
            "app_url": APP_URL,
            "expenses": expenses,
            "today": datetime.now(tz=UTC),
        }
        return application.templates.TemplateResponse(
            request=request,
            name="homepage.html",
            context=context,
        )

    _ = homepage
    return webpage_router
