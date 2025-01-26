from dataclasses import dataclass

from fastapi import FastAPI

from autoexpense3.models.repository import Repository


@dataclass
class Application:
    """Application components."""

    fastapi: FastAPI
    repository: Repository
