from collections.abc import Generator

import pytest
from playwright.sync_api import Page


@pytest.fixture
def homepage(
    page: Page, url: str, real_web_application: Generator[None, None, None]
) -> Page:
    _ = real_web_application
    page.goto(url)
    return page
