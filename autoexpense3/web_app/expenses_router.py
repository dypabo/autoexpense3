from datetime import UTC
from datetime import datetime
from typing import Annotated
from uuid import UUID
from uuid import uuid4

from fastapi import Form
from fastapi import Header
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi.routing import APIRouter

from autoexpense3.models.expense import Expense
from autoexpense3.web_app.application import Application


def build_expenses_router(application: Application) -> APIRouter:
    """Build the expenses router."""
    expenses_router = APIRouter(prefix="/expenses")

    @expenses_router.get("/")
    def expenses(hx_request: Annotated[str | None, Header] = None) -> Response:
        """Get a list of expenses from application repository."""
        if hx_request:
            return HTMLResponse("")
        return JSONResponse([
            e.jsonify() for e in application.repository.get_expenses()
        ])

    @expenses_router.post("/")
    def new_expense(
        request: Request,
        new_expense_date: Annotated[str, Form()],
        new_expense_seller: Annotated[str, Form()],
        new_expense_total: Annotated[float, Form()],
    ) -> Response:
        """Add new expense endpoint."""
        date = f"{new_expense_date}:{UTC}"
        expense = Expense(
            uuid=uuid4(),
            timestamp=datetime.strptime(date, "%Y-%m-%d:%Z").replace(tzinfo=UTC),
            seller=new_expense_seller,
            total=new_expense_total,
        )
        application.repository.add_expense(expense)
        return application.templates.TemplateResponse(
            request=request, name="fragment_expenses.html", context={"expense": expense}
        )

    @expenses_router.delete("/{uuid}")
    def remove_expense(
        uuid: UUID,
    ) -> Response:
        application.repository.remove_expense(uuid)
        return Response()

    _ = expenses
    _ = new_expense
    _ = remove_expense
    return expenses_router
