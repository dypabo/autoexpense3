from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from autoexpense3.models.repository import RepositoryDict
from autoexpense3.web_app.application import Application
from autoexpense3.web_app.expenses_router import build_expenses_router
from autoexpense3.web_app.webpage_router import build_webpage_router

_app = FastAPI()
_templates = Jinja2Templates("autoexpense3/web_app/templates")
_repository = RepositoryDict()

application = Application(_app, _repository, _templates)
_app.include_router(build_expenses_router(application))
_app.include_router(build_webpage_router(application))
