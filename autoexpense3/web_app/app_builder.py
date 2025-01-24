from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from autoexpense3.web_app.constants import APP_NAME


def builder() -> FastAPI:
    """Return a FastAPI application."""
    app = FastAPI()

    @app.get("/")
    def homepage() -> HTMLResponse:
        return HTMLResponse(
            f"""
            <html>
            <title>{APP_NAME}</title>
            <body>Under construction</body>
            </html>
            """,
        )

    return app
