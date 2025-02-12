import subprocess  # noqa: S404
import time
from collections.abc import Generator
from os import environ
from pathlib import Path

import pytest
from playwright.sync_api import Page

from autoexpense3.web_app.constants import APP_URL
from tests.utilities import kill_process_and_children


@pytest.fixture(autouse=True, scope="session")
def web_application() -> Generator[None, None, None]:
    cmd = "uv run fastapi dev"
    with subprocess.Popen(cmd, cwd=Path.cwd(), shell=True) as proc:  # noqa: S602
        time.sleep(3)
        yield
        kill_process_and_children(proc.pid)


@pytest.fixture
def url() -> str:
    if environ.get("GITHUB"):
        return APP_URL
    return "http://127.0.0.1:8000"


@pytest.fixture
def homepage(page: Page, url: str) -> Page:
    page.goto(url)
    return page
