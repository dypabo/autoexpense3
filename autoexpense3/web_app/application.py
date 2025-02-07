from dataclasses import dataclass

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from autoexpense3.models.repository import Repository


@dataclass
class Application:
    """Application components."""

    app: FastAPI
    repository: Repository
    templates: Jinja2Templates
