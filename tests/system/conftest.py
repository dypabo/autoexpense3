import subprocess  # noqa: S404
import time
from collections.abc import Generator
from pathlib import Path

import psutil
import pytest
from playwright.sync_api import Page


def kill_process_and_children(pid: int) -> None:
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()


@pytest.fixture(autouse=True, scope="session")
def web_application() -> Generator[None, None, None]:
    cmd = "uv run fastapi dev"
    with subprocess.Popen(cmd, cwd=Path.cwd(), shell=True) as proc:  # noqa: S602
        time.sleep(3)
        yield
        kill_process_and_children(proc.pid)


@pytest.fixture
def homepage(page: Page) -> Page:
    page.goto("http://127.0.0.1:8000")
    return page
