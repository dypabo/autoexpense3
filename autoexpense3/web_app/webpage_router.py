from datetime import UTC
from datetime import datetime
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter
from fastapi import Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.responses import Response

from autoexpense3.models.user import User
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
        context = {
            "app_name": APP_NAME,
            "app_url": APP_URL,
            "expenses": expenses,
            "today": datetime.now(tz=UTC),
        }
        return application.templates.TemplateResponse(
            request=request,
            name="expenses.html",
            context=context,
        )

    @webpage_router.get("/login")
    def login(request: Request) -> HTMLResponse:
        """User route request processor."""
        context = {
            "app_name": APP_NAME,
            "app_url": APP_URL,
        }
        return application.templates.TemplateResponse(
            request=request,
            name="login.html",
            context=context,
        )

    @webpage_router.post("/login")
    def login_user(
        request: Request,
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
    ) -> Response:
        """User route request processor."""
        _ = request
        _ = email
        _ = password
        response = JSONResponse({})
        response.headers["HX-Redirect"] = "/user"
        return response

    @webpage_router.get("/register")
    def register(request: Request) -> HTMLResponse:
        """User route request processor."""
        context = {
            "app_name": APP_NAME,
            "app_url": APP_URL,
        }
        return application.templates.TemplateResponse(
            request=request,
            name="register.html",
            context=context,
        )

    @webpage_router.post("/register")
    def register_new_user(
        request: Request,
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
    ) -> Response:
        """User route request processor."""
        _ = request
        application.repository.add_user(User(uuid4(), email, password))
        response = JSONResponse({})
        response.headers["HX-Redirect"] = "/login"
        return response

    _ = user
    _ = homepage
    _ = register
    _ = register_new_user
    _ = login
    _ = login_user
    return webpage_router
